
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.frame_message import FrameMessage
from utils.events.src.messages.face_message import FaceMessage
from utils.events.src.messages.marshalling import encode, decode
from utils.video_storage import StorageFactory, StorageType
from utils.image_processing.src.image_serialization import image_debug, draw_boxes, bytestring_to_image, image_to_bytestring
from utils.tracing.src.tracer import get_context, get_tracer
from .face_detector_factory import FaceDetectorFactory
from logging import getLogger

logger = getLogger(__name__)


class FaceDetectionTask:
    def __init__(self, debug_mode,
                 face_detector_configuration,
                 publisher_to_classifier_configuration,
                 storage_configuration,
                 tracer_configuration):

        self.debug = debug_mode

        storage_factory = StorageFactory(**storage_configuration)
        self.frame_storage = storage_factory.new(StorageType.VIDEO_FRAMES)
        self.face_storage = storage_factory.new(StorageType.FRAME_FACES)

        self.face_detector = FaceDetectorFactory.build(face_detector_configuration)
        self.tracer = get_tracer(**tracer_configuration, service_name='argus-detector')
        self.publisher_to_classifier = Publisher.new(**publisher_to_classifier_configuration)

    def close(self):
        self.face_detector.close()
        # self.db.close()

    def execute_with(self, message):
        frame_message: FrameMessage = decode(FrameMessage, message)

        with self.tracer.start_as_current_span('detector', context=get_context(frame_message.trace)):

            # Get frame image
            with self.tracer.start_as_current_span('fetch-frame'):
                frame = bytestring_to_image(self.frame_storage.fetch(str(frame_message)))

            # Convert to cv2 img
            # frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Print frame
            if self.debug:
                image_debug("frame", frame, 1)

            # Detect faces
            with self.tracer.start_as_current_span('detect-faces'):
                bounding_boxes = self.face_detector.detect_face_image(frame)

            # Queue Face Classification messages for each found face
            with self.tracer.start_as_current_span('publish-faces'):
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

                    face_num = 1
                    for bounding_box in bounding_boxes:

                        # Get cropped face
                        x1, y1, x2, y2 = bounding_box
                        cropped_face = frame[y1:y2, x1:x2]

                        # Queue face embedding job
                        face_message = FaceMessage(video_chunk_id=frame_message.video_chunk,
                                                   offset=frame_message.offset,
                                                   timestamp=frame_message.timestamp,
                                                   face_num=face_num,
                                                   bounding_box=bounding_box,
                                                   trace=frame_message.trace)
                        self.face_storage.store(name=str(face_message), data=image_to_bytestring(cropped_face))
                        self.publisher_to_classifier.publish(encode(face_message))

        logger.info("Finished processing message - %s, found %d faces", str(frame_message), len(bounding_boxes))
