from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.face_message import FaceMessage
from utils.events.src.messages.detected_face_message import DetectedFaceMessage
from utils.events.src.messages.matched_face_message import MatchedFaceMessage
from utils.events.src.messages.unknown_face_message import UnknownFaceMessage
from utils.events.src.messages.marshalling import encode, decode
from utils.events.src.messages.helper import unwrap_video_chunk_id
from utils.orm.src.models.person import get_person
from .face_classifier_factory import FaceClassifierFactory
from .face_embedder_factory import FaceEmbedderFactory
from utils.video_storage import StorageFactory, StorageType
from utils.tracing.src.tracer import get_context, get_tracer
from utils.image_processing.src.image_serialization import bytestring_to_image
from utils.orm.src.models import Camera, Face, VideoChunk
from logging import getLogger

FACE_CLASSIFIER_MODEL_KEY = 'model'
FACE_CLASSIFIER_THRESHOLD_KEY = 'threshold'
FACE_CLASSIFIER_MINIO_KEY = 'minio'

UNKNOWN = 'UNKNOWN'

logger = getLogger(__name__)


class FaceClassificationTask:
    def __init__(self, face_classifier_configuration,
                 face_embedder_configuration,
                 publisher_to_web_configuration,
                 publisher_to_warden_configuration,
                 publisher_to_clusterer_configuration,
                 storage_configuration,
                 tracer_configuration):

        self.threshold = face_classifier_configuration[FACE_CLASSIFIER_THRESHOLD_KEY]

        if face_classifier_configuration[FACE_CLASSIFIER_MINIO_KEY] != '':
            people_storage = StorageFactory(**storage_configuration).new(StorageType.PEOPLE)
            people_storage.fetch(face_classifier_configuration[FACE_CLASSIFIER_MINIO_KEY],
                                 face_classifier_configuration[FACE_CLASSIFIER_MODEL_KEY])
        self.face_classifier = FaceClassifierFactory.build(face_classifier_configuration)
        self.face_embedder = FaceEmbedderFactory.build(face_embedder_configuration)

        self.publisher_to_web = Publisher.new(**publisher_to_web_configuration)
        self.publisher_to_warden = Publisher.new(**publisher_to_warden_configuration)
        self.publisher_to_clusterer = Publisher.new(**publisher_to_clusterer_configuration)
        self.face_storage = StorageFactory(**storage_configuration).new(StorageType.FRAME_FACES)
        self.tracer = get_tracer(**tracer_configuration, service_name='argus-classifier')

    def close(self):
        self.face_embedder.close()

    def execute_with(self, message):
        face_message: FaceMessage = decode(FaceMessage, message)

        with self.tracer.start_as_current_span('classifier', context=get_context(face_message.trace)):
            with self.tracer.start_as_current_span('fetch-face'):
                face = bytestring_to_image(self.face_storage.fetch(str(face_message)))

            with self.tracer.start_as_current_span('face-embedding'):
                embedding = self.face_embedder.get_embedding_mem(face)

            with self.tracer.start_as_current_span('face-classification'):
                classification_index, classification_probability = self.face_classifier.predict(embedding)

                is_match = classification_probability > self.threshold

                if classification_index is not None:
                    person_id = int(self.face_classifier.get_name(classification_index))
                    name = get_person(person_id).name
                else:
                    person_id = None
                    name = UNKNOWN

            with self.tracer.start_as_current_span('insert-db-detected-face'):
                camera_name, timestamp = unwrap_video_chunk_id(face_message.video_chunk_id)

                cam_query = Camera.select(Camera.id).where(Camera.alias == camera_name)
                video_chunk_id_query = (VideoChunk
                                        .select(VideoChunk.id)
                                        .where((VideoChunk.camera_id == cam_query) &
                                               (VideoChunk.timestamp == timestamp)))

                face_id = Face.insert(video_chunk_id=video_chunk_id_query,
                                      offset=face_message.offset,
                                      timestamp=face_message.timestamp,
                                      face_num=face_message.face_num,
                                      embedding=list(embedding.astype(float)),
                                      person_id=person_id,
                                      bounding_box=face_message.bounding_box,
                                      probability=classification_probability,
                                      is_match=is_match).execute()

            with self.tracer.start_as_current_span('publish-detected-face'):
                detected_face_message = DetectedFaceMessage(video_chunk_id=face_message.video_chunk_id,
                                                            offset=face_message.offset,
                                                            timestamp=face_message.timestamp,
                                                            face_num=face_message.face_num,
                                                            name=name,
                                                            person_id=person_id,
                                                            bounding_box=face_message.bounding_box,
                                                            probability=classification_probability,
                                                            is_match=is_match,
                                                            trace=face_message.trace)
                self.publisher_to_web.publish(encode(detected_face_message))

                # Queue face data for warden rules processing
                matched_face_message = MatchedFaceMessage(face_id=str(face_id), trace=face_message.trace)
                self.publisher_to_warden.publish(encode(matched_face_message))

        logger.info("Finished - %s, found: %s with prob: %.2f", face_message, name, classification_probability)
