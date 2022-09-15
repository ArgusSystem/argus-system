from ..utils.events.src.message_clients.rabbitmq.client import Client
from ..utils.events.src.message_clients.rabbitmq.management import setup_queue, setup_exchange, queue_bind

# Create RabbitMQ exchanges, queues and binds

rabbitmq_client = Client('localhost', 'argus', 'panoptes')

queues_by_exchange = {
    'argus': ['video-chunks']
}

with rabbitmq_client.channel() as channel:
    for exchange, queues in queues_by_exchange.items():
        setup_exchange(channel, exchange)

        for queue in queues:
            setup_queue(channel, queue)
            queue_bind(channel, exchange, queue, '')

# TODO: Create bucket
