from minio import Minio
from minio.commonconfig import CopySource
from minio.deleteobjects import DeleteObject


class Client:

    def __init__(self, host, port, access_key, secret_key):
        self._client = Minio(f'{host}:{port}',
                             access_key=access_key,
                             secret_key=secret_key,
                             secure=False)

    def make_bucket(self, name):
        self._client.make_bucket(name)

    def exists_bucket(self, name):
        return self._client.bucket_exists(name)

    def remove_bucket(self, name):
        self._client.remove_bucket(name)

    def store(self, bucket, name, data, size, metadata):
        self._client.put_object(bucket, name, data=data, length=size, metadata=metadata)

    def store_file(self, bucket, name, filepath, metadata):
        self._client.fput_object(bucket, name, filepath, metadata=metadata)

    def fetch(self, bucket, name):
        return self._client.get_object(bucket, name).data

    def fetch_file(self, bucket, name, filepath):
        self._client.fget_object(bucket, name, filepath)

    def remove(self, bucket, *names):
        errors = self._client.remove_objects(bucket, map(lambda x: DeleteObject(x), names))

        for error in errors:
            print(error)

    # Costly operation, needs to copy and delete because there is no rename
    def rename(self, bucket, old_name, new_name):
        self._client.copy_object(bucket, new_name, CopySource(bucket, old_name))
        self.remove(bucket, old_name)

    def list(self, bucket):
        return self._client.list_objects(bucket)

