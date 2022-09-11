from minio import Minio


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

    def store(self, bucket, name, data, size):
        self._client.put_object(bucket, name, data=data, length=size)

    def store_file(self, bucket, name, filepath):
        self._client.fput_object(bucket, name, filepath)

    def fetch(self, bucket, name):
        return self._client.get_object(bucket, name).data

    def fetch_file(self, bucket, name, filepath):
        self._client.fget_object(bucket, name, filepath)

    def remove(self, bucket, name):
        self._client.remove_object(bucket, name)
