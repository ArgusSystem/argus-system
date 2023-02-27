from utils.video_storage import StorageType
from utils.video_storage.src.client import Client
from minio.error import S3Error


class MinioService:
    def __init__(self, host):
        self.client = Client(host, 9500, 'argus', 'panoptes')

    def setup(self):
        for storage_type in StorageType:
            bucket = storage_type.value

            if not self.client.exists_bucket(bucket):
                self.client.make_bucket(bucket)

    def clean(self):
        for storage_type in StorageType:
            bucket = storage_type.value

            objects = self.client.list(bucket)
            try:
                self.client.remove(bucket, *map(lambda x: x.object_name, objects))
            except S3Error as error:
                print(error)
