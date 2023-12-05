from utils.events.src.messages.frame_message import FrameMessage
from utils.events.src.messages.marshalling import decode
from utils.video_storage import StorageFactory, StorageType
from utils.image_processing.src.image_serialization import image_debug, draw_boxes, bytestring_to_image, \
    image_to_bytestring
from utils.tracing.src.tracer import get_context, get_tracer
from logging import getLogger

from .face_detector_factory import FaceDetectorFactory
from .notifier_factory import create_notifier

logger = getLogger(__name__)


class FaceDetectionTask:

    MIN_PIXELS_KEY = 'min_pixels'

    def __init__(self, debug_mode,
                 face_detector_configuration,
                 notifier_configuration,
                 storage_configuration,
                 tracer_configuration):

        self.debug = debug_mode

        storage_factory = StorageFactory(**storage_configuration)
        self.frame_storage = storage_factory.new(StorageType.VIDEO_FRAMES)
        self.face_storage = storage_factory.new(StorageType.FRAME_FACES)

        self.face_detector = FaceDetectorFactory.build(face_detector_configuration)
        self.face_min_pixels = face_detector_configuration[FaceDetectionTask.MIN_PIXELS_KEY] if FaceDetectionTask.MIN_PIXELS_KEY in face_detector_configuration else 0
        self.notifier = create_notifier(notifier_configuration)

        self.tracer = get_tracer(**tracer_configuration, service_name='argus-detector')

    def close(self):
        self.face_detector.close()

    def execute_with(self, message):
        frame_message: FrameMessage = decode(FrameMessage, message)

        with self.tracer.start_as_current_span('detector', context=get_context(frame_message.trace)):
            # Get frame image
            with self.tracer.start_as_current_span('fetch-frame'):
                frame = bytestring_to_image(self.frame_storage.fetch(str(frame_message)))

            # Print frame
            if self.debug:
                image_debug("frame", frame, 1)

            # Detect faces
            with self.tracer.start_as_current_span('detect-faces'):
                bounding_boxes = self.face_detector.detect_face_image(frame)

            # Queue Face Classification messages for each found face
            with self.tracer.start_as_current_span('publish-faces'):
                if len(bounding_boxes) > 0:
                    if self.debug:
                        image_debug("detected faces", draw_boxes(frame, bounding_boxes), 1)

                    face_num = 1
                    for bounding_box in bounding_boxes:
                        # Store cropped face
                        x1, y1, x2, y2 = bounding_box
                        w = x2 - x1
                        h = y2 - y1
                        pixels = w * h
                        if pixels < self.face_min_pixels:
                            continue
                        cropped_face = frame[y1:y2, x1:x2]
                        object_name = f'{frame_message.video_chunk}-{frame_message.offset}-{face_num}'
                        self.face_storage.store(name=object_name, data=image_to_bytestring(cropped_face))

                        # Notify detection information
                        self.notifier.notify(video_chunk=frame_message.video_chunk,
                                             offset=frame_message.offset,
                                             timestamp=frame_message.timestamp,
                                             face_num=face_num,
                                             bounding_box=bounding_box,
                                             trace=frame_message.trace)
                        face_num += 1

        logger.info("Finished processing message - %s, found %d faces", str(frame_message), len(bounding_boxes))
