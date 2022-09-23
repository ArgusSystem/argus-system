
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.frame_message import FrameMessage
from utils.events.src.messages.face_message import FaceMessage
from utils.events.src.messages.marshalling import encode, decode
from utils.image_processing.src.image_serialization import image_debug, draw_boxes, image_to_bytestring
from .face_detector_factory import FaceDetectorFactory
import cv2
import numpy as np
import logging

PUBLISHER_KEY = 'publisher'
DETECTOR_KEY = 'face_detector'
DEBUG_KEY = 'debug'


class FaceDetectionTask:
    def __init__(self, configuration):
        self.face_detector = FaceDetectorFactory.build(**configuration[DETECTOR_KEY])
        self.publisher_to_classifier = Publisher.new(**configuration[PUBLISHER_KEY])
        self.debug = configuration[DEBUG_KEY]
        # self.db = Database(self.configuration['db'])

    def close(self):
        self.face_detector.close()
        # self.db.close()

    def execute_with(self, message):
        face_detection_message: FrameMessage = decode(FrameMessage, message)

        # Get message
        video_chunk_id = face_detection_message.video_chunk_id
        frame_id = face_detection_message.frame_id
        frame = face_detection_message.payload

        # Convert to cv2 img
        #frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Print frame
        if self.debug:
            image_debug("frame", frame, 1, cv2.COLOR_RGB2BGR)

        # Detect faces
        print("- Performing detection - frame_id: " + str(frame_id) + " - video chunk id: " + str(video_chunk_id))
        logging.debug("- Performing detection - frame_id: " + str(frame_id) + " - video chunk id: " + str(video_chunk_id))

        rects = self.face_detector.detect_face_image(frame)
        if len(rects) > 0:
            # faces = []
            # for rect in rects:
            #     x1, y1, x2, y2 = rect
            #     db_rect = [[x1, y1], [x2, y2]]
            #
            #     Insert detected face to db
            #     face = Face(frame_id=frame_id, bounding_box=db_rect)
            #     self.db.add(face)
            #     faces.append(face)

            if self.debug:
                image_debug("detected faces", draw_boxes(frame, rects), 1, cv2.COLOR_RGB2BGR)

            # for rect, face in zip(rects, faces):
            for rect in rects:

                # Get cropped face
                x1, y1, x2, y2 = rect
                cropped_face = frame[y1:y2, x1:x2]

                logging.debug("- Found face, assigned id: " + str('face.id') + " - video chunk id: " + str(video_chunk_id))
                print("- Found face, assigned id: " + str('face.id') + " - video chunk id: " + str(video_chunk_id))

                # Queue face embedding job
                face_embedding_message = FaceMessage(video_chunk_id, 'face.id', image_to_bytestring(cropped_face))
                self.publisher_to_classifier.publish(encode(face_embedding_message))
