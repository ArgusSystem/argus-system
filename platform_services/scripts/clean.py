from utils.orm.src.management import create_tables, drop_tables
from utils.events.src.message_clients.rabbitmq.management import queue_purge
from utils.video_storage import StorageType
from .clients.postgresql import db
from .clients.minio import client as storage_client
from .clients.rabbitmq import client as rabbitmq_client, queues_by_exchange


# Purge messages from all queues

with rabbitmq_client.channel() as channel:
    for exchange, queues in queues_by_exchange.items():
        for queue in queues:
            queue_purge(channel, queue)

# Remove all objects from buckets

for storage_type in StorageType:
    bucket = storage_type.value

    objects = storage_client.list(bucket)
    storage_client.remove(bucket, *map(lambda x: x.object_name, objects))

# Re-create PostgreSQL tables

drop_tables(db)
create_tables(db)
