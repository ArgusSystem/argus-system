from .local_video import delete_video
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.marshalling import encode
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.video_storage.src.storage import get_video_chunks_storage

ID_KEY = 'id'
PUBLISHER_KEY = 'publisher'
STORAGE_KEY = 'storage'


class VideoPublisher:

    def __init__(self, input_queue, configuration):
        self.input_queue = input_queue
        self.camera_id = configuration[ID_KEY]
        self.publisher = Publisher.new(**configuration[PUBLISHER_KEY])
        self.storage = get_video_chunks_storage(configuration[STORAGE_KEY])

    def publish(self, is_running):
        while is_running():
            self.input_queue.compute(self._publish)

    def _publish(self, video_metadata):
        message = VideoChunkMessage(self.camera_id, video_metadata.timestamp)

        # Store video chunk in the cloud
        self.storage.store(str(message), video_metadata.filename)

        # Send event of new video chunk
        self.publisher.publish(encode(message))

        # Delete local video chunk
        delete_video(video_metadata.filename)
