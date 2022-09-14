from .client import Client
from .storage_type import StorageType


class Storage:

    def __init__(self, client_configuration, bucket):
        self.client = Client(**client_configuration)
        self.bucket = bucket

    def store_file(self, name, filepath):
        self.client.store_file(self.bucket, name, filepath)

    def retrieve_file(self, name, filepath):
        self.client.fetch_file(self.bucket, name, filepath)


def get_video_chunks_storage(client_configuration):
    return Storage(client_configuration, StorageType.VIDEO_CHUNKS.value)


def get_video_frames_storage(client_configuration):
    return Storage(client_configuration, StorageType.VIDEO_FRAMES.value)
