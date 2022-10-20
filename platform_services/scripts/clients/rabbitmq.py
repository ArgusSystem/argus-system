from utils.events.src.message_clients.rabbitmq.client import Client as RabbitMQClient


client = RabbitMQClient('localhost', 'argus', 'panoptes')

queues_by_exchange = {
    'argus': ['new_video_chunks', 'published_video_chunks', 'frames', 'faces', 'published_detected_faces']
}
