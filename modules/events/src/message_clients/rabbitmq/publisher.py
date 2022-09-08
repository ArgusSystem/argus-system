import pika
import logging


class Publisher:

    def __init__(self, configuration):
        self.host = configuration['host']
        self.exchange = configuration['exchange']
        self.routing_key = configuration['routing_key']
        
        self.credentials = pika.PlainCredentials(configuration['username'], configuration['password'])
        self.parameters = pika.ConnectionParameters(host=self.host, credentials=self.credentials)
        self._connect()

    def publish(self, message):
        try:
            self._publish(message)
        except pika.exceptions.StreamLostError as e:
            logging.warning(e)
            self._connect()
            self._publish(message)

    def _publish(self, message):
        self.channel.basic_publish(self.exchange, self.routing_key, message)

    def _connect(self):
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
