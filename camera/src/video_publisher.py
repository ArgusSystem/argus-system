from logging import getLogger

from .local_video import delete_video
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.marshalling import encode
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.video_storage import StorageFactory, StorageType
from utils.tracing import timer

ID_KEY = 'id'
PUBLISHER_KEY = 'publisher'
STORAGE_KEY = 'storage'

logger = getLogger(__name__)


class VideoPublisher:

    def __init__(self, input_queue, configuration):
        self.input_queue = input_queue
        self.camera_id = configuration[ID_KEY]
        self.publisher = Publisher.new(**configuration[PUBLISHER_KEY])
        self.storage = StorageFactory(**configuration[STORAGE_KEY]).new(StorageType.VIDEO_CHUNKS)

    def publish(self, is_running):
        while is_running():
            self.input_queue.compute(self._publish)

    @timer(logger, 'Process video chunk')
    def _publish(self, video_metadata):
        message = VideoChunkMessage(camera_id=self.camera_id,
                                    timestamp=video_metadata.timestamp,
                                    encoding=video_metadata.encoding,
                                    framerate=video_metadata.framerate,
                                    width=video_metadata.resolution[0],
                                    height=video_metadata.resolution[1])

        # Store video chunk in the cloud
        self.storage.store(name=str(message),
                           filepath=video_metadata.filename)

        # Send event of new video chunk
        self.publisher.publish(encode(message))

        # Delete local video chunk
        delete_video(video_metadata.filename)
