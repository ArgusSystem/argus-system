from time import time
from .local_video import get_filepath

FORMAT = 'h264'


class VideoMetadata:

    def __init__(self, filepath=get_filepath):
        self.timestamp = time()
        self.filename = filepath(self.timestamp, FORMAT)
