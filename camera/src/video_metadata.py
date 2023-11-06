from time import time_ns
from .local_video import get_filepath
from .sequence_generator import SequenceGenerator

ENCODING = 'h264'
SEQUENCE_GENERATOR = SequenceGenerator()


class VideoMetadata:

    def __init__(self, duration, timestamp=None, encoding=ENCODING, filepath=get_filepath):
        self.timestamp = timestamp or (time_ns() // 1_000_000)  # EPOCH UTC IN MS
        self.filename = filepath(self.timestamp, encoding)
        self.encoding = encoding
        self.duration = duration
        self.sequence_id = SEQUENCE_GENERATOR.get()
