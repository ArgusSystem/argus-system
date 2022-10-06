from time import time_ns
from .local_video import get_filepath

ENCODING = 'h264'


class VideoMetadata:

    def __init__(self, camera_id, framerate, resolution, filepath=get_filepath):
        self.camera_id = camera_id
        self.timestamp = time_ns() // 1_000_000
        self.filename = filepath(self.timestamp, ENCODING)
        self.encoding = ENCODING
        self.framerate = framerate
        self.resolution = resolution

    def id(self):
        return f'{self.camera_id}-{self.timestamp}'
