from contextlib import contextmanager
import ssl

from pika import BlockingConnection, ConnectionParameters, PlainCredentials, SSLOptions
from pika.exceptions import StreamLostError


class Client:

    def __init__(self, host, username, password, ssl_ca=None):
        ssl_context = None
        ssl_options = None
        if ssl_ca:
            ssl_context = ssl.create_default_context(cafile=ssl_ca)
            ssl_options = SSLOptions(context=ssl_context)
        self._parameters = ConnectionParameters(
            host=host,
            credentials=PlainCredentials(username, password),
            ssl_options=ssl_options)

        self._connect()

    def _connect(self):
        self._connection = BlockingConnection(parameters=self._parameters)
        self._new_channel()

    def _new_channel(self):
        self._channel = self._connection.channel()
        self._channel.basic_qos(prefetch_count=10)

    @contextmanager
    def channel(self):
        try:
            self._connection.sleep(0.001)
        except StreamLostError:
            self._connect()

        if self._channel.is_closed:
            self._new_channel()

        yield self._channel

    def close(self):
        self._channel.close()
        self._connection.close()
