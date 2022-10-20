from .clients.rabbitmq import client as rabbitmq_client, queues_by_exchange
from .clients.minio import client as storage_client
from .clients.postgresql import db

from utils.events.src.message_clients.rabbitmq.management import setup_queue, setup_exchange, queue_bind
from utils.orm.src.management import create_tables
from utils.video_storage.src.storage_type import StorageType

# Create RabbitMQ exchanges, queues and binds

with rabbitmq_client.channel() as channel:
    for exchange, queues in queues_by_exchange.items():
        setup_exchange(channel, exchange)

        for queue in queues:
            setup_queue(channel, queue)
            queue_bind(channel, queue, exchange, queue)

# Create Minio buckets

for storage_type in StorageType:
    bucket = storage_type.value

    if not storage_client.exists_bucket(bucket):
        storage_client.make_bucket(bucket)

# Create PostgreSQL tables

create_tables(db)

