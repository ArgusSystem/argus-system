
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.frame_message import FrameMessage
from utils.events.src.messages.face_message import FaceMessage
from utils.events.src.messages.marshalling import encode, decode
from utils.video_storage import StorageFactory, StorageType
from utils.image_processing.src.image_serialization import image_debug, draw_boxes, bytestring_to_image, image_to_bytestring
from .face_detector_factory import FaceDetectorFactory
from logging import getLogger

PUBLISHER_KEY = 'publisher'
DETECTOR_KEY = 'face_detector'
DEBUG_KEY = 'debug'
STORAGE_KEY = 'storage'


class FaceDetectionTask:
    def __init__(self, configuration):
        self.face_detector = FaceDetectorFactory.build(**configuration[DETECTOR_KEY])
        self.publisher_to_classifier = Publisher.new(**configuration[PUBLISHER_KEY])
        self.debug = configuration[DEBUG_KEY]
        self.frame_storage = StorageFactory(**configuration[STORAGE_KEY]).new(StorageType.VIDEO_FRAMES)
        self.face_storage = StorageFactory(**configuration[STORAGE_KEY]).new(StorageType.FRAME_FACES)
        self.logger = getLogger(__name__)

    def close(self):
        self.face_detector.close()
        # self.db.close()

    def execute_with(self, message):
        frame_message: FrameMessage = decode(FrameMessage, message)

        self.logger.debug("Processing message - %s", str(frame_message))

        # Get frame image
        frame = bytestring_to_image(self.frame_storage.fetch(str(frame_message)))

        # Convert to cv2 img
        # frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Print frame
        if self.debug:
            image_debug("frame", frame, 1)

        # Detect faces
        bounding_boxes = self.face_detector.detect_face_image(frame)
        self.logger.debug("Found %d faces", len(bounding_boxes))

        if len(bounding_boxes) > 0:
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
                image_debug("detected faces", draw_boxes(frame, bounding_boxes), 1)

            # for rect, face in zip(rects, faces):
            face_num = 1
            for bounding_box in bounding_boxes:

                # Get cropped face
                x1, y1, x2, y2 = bounding_box
                cropped_face = frame[y1:y2, x1:x2]

                # Queue face embedding job
                face_message = FaceMessage(frame_message.video_chunk, frame_message.offset, face_num, bounding_box)
                self.face_storage.store(name=str(face_message), data=image_to_bytestring(cropped_face))
                self.publisher_to_classifier.publish(encode(face_message))

        self.logger.debug("Finished - %s", str(frame_message))
