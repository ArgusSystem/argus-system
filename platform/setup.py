from utils.events.src.message_clients.rabbitmq.client import Client as RabbitMQClient
from utils.events.src.message_clients.rabbitmq.management import setup_queue, setup_exchange, queue_bind
from utils.video_storage.src.client import Client as StorageClient
from utils.video_storage.src.storage_type import StorageType

# Create RabbitMQ exchanges, queues and binds

rabbitmq_client = RabbitMQClient('localhost', 'argus', 'panoptes')

queues_by_exchange = {
    'argus': ['new_video_chunks', 'published_video_chunks', 'frames', 'faces', 'published_detected_faces']
}

with rabbitmq_client.channel() as channel:
    for exchange, queues in queues_by_exchange.items():
        setup_exchange(channel, exchange)

        for queue in queues:
            setup_queue(channel, queue)
            queue_bind(channel, queue, exchange, queue)

# Create Minio buckets

storage_client = StorageClient('localhost', 9500, 'argus', 'panoptes')

for storage_type in StorageType:
    bucket = storage_type.value

    if not storage_client.exists_bucket(bucket):
        storage_client.make_bucket(bucket)
