
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.face_message import FaceMessage
from utils.events.src.messages.detected_face_message import DetectedFaceMessage
from utils.events.src.messages.marshalling import encode, decode
from utils.events.src.messages.helper import get_camera_id, get_timestamp
from .face_classifier_factory import FaceClassifierFactory
from .face_embedder_factory import FaceEmbedderFactory
from utils.video_storage import StorageFactory, StorageType
from utils.tracing.src.tracer import get_context, get_tracer
from utils.image_processing.src.image_serialization import bytestring_to_image
from utils.orm.src.models import Face, VideoChunk, Person
from utils.orm.src.models.camera import get_camera
from logging import getLogger

FACE_CLASSIFIER_MODEL_KEY = 'model'
FACE_CLASSIFIER_THRESHOLD_KEY = 'threshold'
FACE_CLASSIFIER_MINIO_KEY = 'minio'

logger = getLogger(__name__)


class FaceClassificationTask:
    def __init__(self, face_classifier_configuration,
                 face_embedder_configuration,
                 publisher_to_web_configuration,
                 publisher_to_summarizer_configuration,
                 storage_configuration,
                 tracer_configuration):

        self.threshold = face_classifier_configuration[FACE_CLASSIFIER_THRESHOLD_KEY]

        if face_classifier_configuration[FACE_CLASSIFIER_MINIO_KEY] != '':
            people_storage = StorageFactory(**storage_configuration).new(StorageType.PEOPLE)
            people_storage.fetch(face_classifier_configuration[FACE_CLASSIFIER_MINIO_KEY], face_classifier_configuration[FACE_CLASSIFIER_MODEL_KEY])
        self.face_classifier = FaceClassifierFactory.build(face_classifier_configuration)
        self.face_embedder = FaceEmbedderFactory.build(face_embedder_configuration)

        self.publisher_to_web = Publisher.new(**publisher_to_web_configuration)
        self.publisher_to_summarizer = Publisher.new(**publisher_to_summarizer_configuration)
        self.face_storage = StorageFactory(**storage_configuration).new(StorageType.FRAME_FACES)
        self.tracer = get_tracer(**tracer_configuration, service_name='argus-classifier')

    def close(self):
        self.face_embedder.close()
        # self.db.close()

    def execute_with(self, message):
        face_message: FaceMessage = decode(FaceMessage, message)

        with self.tracer.start_as_current_span('classifier', context=get_context(face_message.trace)):

            # Get face image
            with self.tracer.start_as_current_span('fetch-face'):
                face = bytestring_to_image(self.face_storage.fetch(str(face_message)))

            # Perform face embedding
            with self.tracer.start_as_current_span('face-embedding'):
                embedding = self.face_embedder.get_embedding_mem(face)

            # Insert result into database
            # face_embedding = FaceEmbedding(face_id=face_id, embedding=list(embedding.astype(float)))
            # self.db.add(face_embedding)

            # Perform face classification
            with self.tracer.start_as_current_span('face-classification'):
                classification_index, classification_probability = self.face_classifier.predict(embedding)
                face_id = int(self.face_classifier.get_name(classification_index))
                is_match = classification_probability > self.threshold
                name = Person.get(Person.id == face_id).name


            # Insert face to database
            with self.tracer.start_as_current_span('insert-db-detected-face'):
                camera_id = get_camera(get_camera_id(face_message.video_chunk_id))
                #print(classification_probability)
                face = Face(video_chunk=VideoChunk.get(VideoChunk.camera == camera_id,
                                                       VideoChunk.timestamp ==
                                                       int(get_timestamp(face_message.video_chunk_id))),
                            offset=face_message.offset,
                            timestamp=face_message.timestamp,
                            person=face_id,
                            bounding_box=face_message.bounding_box,
                            probability=classification_probability,
                            is_match=is_match)
                face.save()

            with self.tracer.start_as_current_span('publish-detected-face'):
                # Queue face data message for web streaming
                detected_face_message = DetectedFaceMessage(video_chunk_id=face_message.video_chunk_id,
                                                            offset=face_message.offset,
                                                            timestamp=face_message.timestamp,
                                                            face_num=face_message.face_num,
                                                            name=name,
                                                            person_id=face_id,
                                                            bounding_box=face_message.bounding_box,
                                                            probability=classification_probability,
                                                            is_match=is_match,
                                                            trace=face_message.trace)
                self.publisher_to_web.publish(encode(detected_face_message))
                if is_match:
                    self.publisher_to_summarizer.publish(encode(detected_face_message))

        logger.info("Finished - %s, found: %s with prob: %.2f", face_message, name, classification_probability)
