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

    def fetch(self, name, encoding):
        filepath = os.path.join(TMP, f'{name}.{encoding}')
        self._remote_storage.fetch(name=name, filepath=filepath)
        return filepath

    def store(self, name, filepath):
        self._remote_storage.store(name=name, filepath=filepath)