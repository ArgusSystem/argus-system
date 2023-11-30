from io import BytesIO


class Storage:

    def __init__(self, client, bucket):
        self.client = client
        self.bucket = bucket

    def store(self, name, data=None, filepath=None, metadata=None):
        if (data or filepath) != (filepath or data):
            raise AttributeError('Must specify only the data or filepath parameter!')

        if data is not None:
            self.client.store(self.bucket, name, BytesIO(data), len(data), metadata)

        if filepath is not None:
            self.client.store_file(self.bucket, name, filepath, metadata)

    def fetch(self, name, filepath=None):
        if filepath is not None:
            self.client.fetch_file(self.bucket, name, filepath)
        else:
            return self.client.fetch(self.bucket, name)

    def list(self):
        return self.client.list(self.bucket)

    def rename(self, old_name, new_name):
        self.client.rename(self.bucket, old_name, new_name)

    def remove(self, name):
        self.client.remove(self.bucket, name)
