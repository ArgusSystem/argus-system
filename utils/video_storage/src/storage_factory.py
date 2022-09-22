from .client import Client
from .storage import Storage


class StorageFactory:

    def __init__(self, host, port, access_key, secret_key):
        self.client = Client(host, port, access_key, secret_key)

    def new(self, storage_type):
        return Storage(self.client, storage_type.value)
