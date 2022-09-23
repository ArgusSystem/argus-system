from time import time_ns
from .local_video import get_filepath

ENCODING = 'h264'


class VideoMetadata:

    def __init__(self, framerate, resolution, filepath=get_filepath):
        self.timestamp = time_ns()
        self.filename = filepath(self.timestamp, ENCODING)
        self.encoding = ENCODING
        self.framerate = framerate
        self.resolution = resolution
