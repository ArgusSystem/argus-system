from utils.video_storage import StorageType
from cv2 import imencode


def _to_bytes(frame, extension='.jpg'):
    ret_val, np_arr = imencode(extension, frame)
    return np_arr.tobytes()


class FrameStorage:

    def __init__(self, storage_factory):
        self.remote_storage = storage_factory.new(StorageType.VIDEO_FRAMES)

    def store(self, name, frame):
        self.remote_storage.store(name=name, data=_to_bytes(frame))
