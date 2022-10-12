import tempfile
import sys

LOCAL_DIR = tempfile.gettempdir()
NULL_DEVICE = 'nul' if sys.platform == 'win32' else '/dev/null'


class LocalVideoChunk:

    def __init__(self, camera_id, timestamp, encoding, framerate, width, height, filepath):
        self.camera_id = camera_id
        self.timestamp = timestamp
        self.encoding = encoding
        self.framerate = framerate
        self.width = width
        self.height = height
        self.filepath = filepath
