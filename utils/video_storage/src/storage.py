from io import BytesIO


class Storage:

    def __init__(self, client, bucket):
        self.client = client
        self.bucket = bucket

    def store(self, name, data=None, filepath=None):
        if (data or filepath) != (filepath or data):
            raise AttributeError('Must specify only the data or filepath parameter!')

        if data is not None:
            self.client.store(self.bucket, name, BytesIO(data), len(data))

        if filepath is not None:
            self.client.store_file(self.bucket, name, filepath)

    def fetch(self, name, filepath=None):
        if filepath is not None:
            self.client.fetch_file(self.bucket, name, filepath)
        else:
            return self.client.fetch(self.bucket, name)

    def remove(self, name):
        self.client.remove(self.bucket, name)
