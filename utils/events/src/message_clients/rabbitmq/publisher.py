from .client import Client


class Publisher:

    def __init__(self, client, exchange, routing_key):
        self.client = client
        self.exchange = exchange
        self.routing_key = routing_key

    @classmethod
    def new(cls, host, username, password, exchange, routing_key):
        return cls(Client(host, username, password), exchange, routing_key)

    def publish(self, message):
        with self.client.channel() as channel:
            channel.basic_publish(self.exchange, self.routing_key, message)
