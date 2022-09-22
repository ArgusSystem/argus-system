class Storage:

    def __init__(self, client, bucket):
        self.client = client
        self.bucket = bucket

    def store(self, name, data=None, filepath=None):
        if (data is None) ^ (filepath is None):
            raise 'Must specify only the data or filepath parameter!'

        if data is not None:
            self.client.store(self.bucket, name, data, len(data))

        if filepath is not None:
            self.client.store_file(self.bucket, name, filepath)

    def fetch(self, name, filepath):
        self.client.fetch_file(self.bucket, name, filepath)

    def remove(self, name):
        self.client.remove(self.bucket, name)
