
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.face_message import FaceMessage
from utils.events.src.messages.detected_face_message import DetectedFaceMessage
from utils.events.src.messages.marshalling import encode, decode
from .classifier_support_vector import SVClassifier
from .face_embedder_factory import FaceEmbedderFactory
from utils.video_storage import StorageFactory, StorageType
from utils.image_processing.src.image_serialization import bytestring_to_image
from logging import getLogger

PUBLISHER_KEY = 'publisher'
FACE_EMBEDDER_KEY = 'face_embedder'
FACE_CLASSIFIER_KEY = 'face_classifier'
STORAGE_KEY = 'storage'


class FaceClassificationTask:
    def __init__(self, configuration):
        self.face_classifier = SVClassifier.load(configuration[FACE_CLASSIFIER_KEY]['model'])
        self.threshold = configuration[FACE_CLASSIFIER_KEY]['threshold']

        self.face_embedder = FaceEmbedderFactory.build(**configuration[FACE_EMBEDDER_KEY])

        # self.db = Database(self.configuration['db'])

        self.publisher_to_web = Publisher.new(**configuration[PUBLISHER_KEY])

        self.face_storage = StorageFactory(**configuration[STORAGE_KEY]).new(StorageType.FRAME_FACES)

        self.logger = getLogger(__name__)

    def close(self):
        self.face_embedder.close()
        # self.db.close()

    def execute_with(self, message):
        face_message: FaceMessage = decode(FaceMessage, message)

        self.logger.debug("Processing message - %s", face_message)

        # Get face
        face = bytestring_to_image(self.face_storage.fetch(str(face_message)))

        # Perform face embedding
        embedding = self.face_embedder.get_embedding_mem(face)

        # Insert result into database
        # face_embedding = FaceEmbedding(face_id=face_id, embedding=list(embedding.astype(float)))
        # self.db.add(face_embedding)

        # Perform face classification
        classification_index, classification_probability = self.face_classifier.predict(embedding)
        name = 'unknown'
        if classification_probability > self.threshold:
            name = self.face_classifier.get_name(classification_index)

        self.logger.debug("Found: %s with prob: %.2f", name, classification_probability)

        # Update database face row with result
        # face: Face = self.db.get(Face, face_id)
        # face.classification_id = int(classification_index)
        # face.probability_classification = float(classification_probability)
        # face.is_match = is_match
        # self.db.update()

        # Queue face data message for web streaming
        detected_face_message = DetectedFaceMessage(face_message.video_chunk_id, face_message.offset,
                                                    face_message.face_num, name, face_message.bounding_box,
                                                    classification_probability)
        self.publisher_to_web.publish(encode(detected_face_message))

        self.logger.debug("Finished - %s", face_message)
