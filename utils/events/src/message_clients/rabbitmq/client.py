from contextlib import contextmanager
from pika import BlockingConnection, ConnectionParameters, PlainCredentials


class Client:

    def __init__(self, host, username, password):
        self._parameters = ConnectionParameters(
            host=host,
            credentials=PlainCredentials(username, password))

        self._connect()

    def _connect(self):
        self._connection = BlockingConnection(parameters=self._parameters)
        self._channel = self._connection.channel()

    @contextmanager
    def channel(self):
        yield self._channel

    def close(self):
        self.channel.close()
        self._connection.close()
