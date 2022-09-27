
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.face_message import FaceMessage
from utils.events.src.messages.marshalling import encode, decode
from .classifier_support_vector import SVClassifier
from .face_embedder_factory import FaceEmbedderFactory
from utils.video_storage import StorageFactory, StorageType
from utils.image_processing.src.image_serialization import bytestring_to_image
import cv2
import numpy as np

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

    def close(self):
        self.face_embedder.close()
        # self.db.close()

    def execute_with(self, message):
        face_message: FaceMessage = decode(FaceMessage, message)

        # Get face
        face_id = face_message.face_id
        video_chunk_id = face_message.video_chunk_id
        face = bytestring_to_image(self.face_storage.fetch(str(face_message)))

        # Perform face embedding
        print("")
        print("- Performing embedding - face_id: " + str(face_id))
        embedding = self.face_embedder.get_embedding_mem(face)

        # Insert result into database
        # face_embedding = FaceEmbedding(face_id=face_id, embedding=list(embedding.astype(float)))
        # self.db.add(face_embedding)

        # Perform face classification
        print("- Performing classification - face_id: " + str(face_id))
        classification_index, classification_probability = self.face_classifier.predict(embedding)
        is_match = classification_probability > self.threshold

        print("- Found: " + self.face_classifier.get_name(classification_index) +
              " with prob: " + str(classification_probability))

        # Update database face row with result
        # face: Face = self.db.get(Face, face_id)
        # face.classification_id = int(classification_index)
        # face.probability_classification = float(classification_probability)
        # face.is_match = is_match
        # self.db.update()

        # Queue face data message for web streaming
        #self.publisher_to_web.publish(encode())

