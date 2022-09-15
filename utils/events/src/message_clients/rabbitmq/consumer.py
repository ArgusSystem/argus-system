from .client import Client
from threading import Event


class Consumer:

    CONSUME_TIMEOUT_S = 1

    def __init__(self, client, queue, on_message_callback):
        self.client = client
        self.queue = queue
        self._on_message_callback = on_message_callback
        self._stop_signal = Event()

    @classmethod
    def new(cls, host, username, password, queue, on_message_callback):
        return cls(Client(host, username, password), queue, on_message_callback)

    def start(self):
        with self.client.channel() as channel:
            for method, _props, body in channel.consume(self.queue, inactivity_timeout=self.CONSUME_TIMEOUT_S):
                if method is not None:
                    self._on_message_callback(body)
                    channel.basic_ack(delivery_tag=method.delivery_tag)

                if self._stop_signal.is_set():
                    channel.cancel()

    def stop(self):
        self._stop_signal.set()
