from utils.video_storage import StorageType
import os

TMP = 'tmp'


def _create_local_storage():
    if not os.path.exists(TMP):
        os.mkdir(TMP)


class VideoStorage:

    def __init__(self, storage_factory):
        _create_local_storage()
        self._remote_storage = storage_factory.new(StorageType.VIDEO_CHUNKS)

    def fetch_video(self, key):
        filepath = os.path.join(TMP, key)
        self._remote_storage.fetch(key, filepath)
        return filepath
