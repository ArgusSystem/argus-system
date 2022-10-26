from utils.video_storage import StorageType
from utils.video_storage.src.client import Client


class MinioService:
    def __init__(self):
        self.client = Client('localhost', 9500, 'argus', 'panoptes')

    def setup(self):
        for storage_type in StorageType:
            bucket = storage_type.value

            if not self.client.exists_bucket(bucket):
                self.client.make_bucket(bucket)

    def clean(self):
        for storage_type in StorageType:
            bucket = storage_type.value

            objects = self.client.list(bucket)
            self.client.remove(bucket, *map(lambda x: x.object_name, objects))
