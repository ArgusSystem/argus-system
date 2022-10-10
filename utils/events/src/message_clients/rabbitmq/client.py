from contextlib import contextmanager

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.exceptions import StreamLostError


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
        try:
            self._connection.sleep(0.01)
        except StreamLostError:
            # print("client: connection is dead, reconnecting")
            self._connect()
        yield self._channel

    def close(self):
        self._channel.close()
        self._connection.close()
