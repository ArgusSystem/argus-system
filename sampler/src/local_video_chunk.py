import tempfile
import sys

LOCAL_DIR = tempfile.gettempdir()
NULL_DEVICE = 'nul' if sys.platform == 'win32' else '/dev/null'


class LocalVideoChunk:

    def __init__(self, camera_id, timestamp, sequence_id, encoding, filepath):
        self.camera_id = camera_id
        self.timestamp = timestamp
        self.sequence_id = sequence_id
        self.encoding = encoding
        self.filepath = filepath
