import logging
from minio import Minio
from minio.error import S3Error


class S3Client:

    def __init__(self, configuration):
        self._host = configuration['host']
        self._port = configuration['port']
        self._access_key = configuration['access_key']
        self._secret_key = configuration['secret_key']
        self.bucket = configuration['bucket']

        self.client = Minio("{}:{}".format(self._host, self._port),
            access_key=self._access_key,
            secret_key=self._secret_key,
            secure=False)

    def store(self, id, data, size):
        try:
            self.client.put_object(self.bucket, str(id), data=data, length=size)
        except S3Error as err:
            logging.exception("Store failed for {}".format(id))
            raise

    def store_file(self, id, filepath):
        try:
            self.client.fput_object(self.bucket, str(id), filepath)
        except S3Error as err:
            logging.exception("Store file failed for {} -> {}".format(id, filepath))
            raise

    def retrieve(self, id):
        try:
            return self.client.get_object(self.bucket, str(id)).data
        except S3Error as err:
            logging.exception("Retrieve failed for {}".format(id))
            raise

    def retrieve_file(self, id, filepath):
        try:
            self.client.fget_object(self.bucket, str(id), filepath)
        except S3Error as err:
            logging.exception("Retrieve file failed for {} -> {}".format(id, filepath))
            raise
