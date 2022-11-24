from time import time_ns
from .local_video import get_filepath
from .sequence_generator import SequenceGenerator

ENCODING = 'h264'
SEQUENCE_GENERATOR = SequenceGenerator()


class VideoMetadata:

    def __init__(self, camera_id, duration, filepath=get_filepath):
        self.camera_id = camera_id
        self.timestamp = time_ns() // 1_000_000
        self.filename = filepath(self.timestamp, ENCODING)
        self.encoding = ENCODING
        self.duration = duration
        self.sequence_id = SEQUENCE_GENERATOR.get()
