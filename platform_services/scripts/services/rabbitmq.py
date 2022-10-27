from utils.events.src.message_clients.rabbitmq.client import Client
from utils.events.src.message_clients.rabbitmq.management import queue_bind, queue_purge, setup_exchange, setup_queue


class RabbitMQService:
    def __init__(self):
        self.client = Client('localhost', 'argus', 'panoptes')

        self.queues_by_exchange = {
            'argus': [
                'new_video_chunks',
                'published_video_chunks',
                'frames',
                'faces',
                'published_detected_faces'
            ]
        }

    def setup(self):
        with self.client.channel() as channel:
            for exchange, queues in self.queues_by_exchange.items():
                setup_exchange(channel, exchange)

                for queue in queues:
                    setup_queue(channel, queue)
                    queue_bind(channel, queue, exchange, queue)

    def clean(self):
        with self.client.channel() as channel:
            for exchange, queues in self.queues_by_exchange.items():
                for queue in queues:
                    queue_purge(channel, queue)