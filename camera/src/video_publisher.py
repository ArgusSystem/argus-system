from logging import getLogger

from utils.tracing.src.tracer import get_context
from .local_video import delete_video
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.marshalling import encode
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.video_storage import StorageFactory, StorageType

logger = getLogger(__name__)


class VideoPublisher:

    def __init__(self, input_queue, tracer, publisher_configuration, storage_configuration):
        self.input_queue = input_queue
        self.tracer = tracer
        self.publisher = Publisher.new(**publisher_configuration)
        self.storage = StorageFactory(**storage_configuration).new(StorageType.VIDEO_CHUNKS)

    def publish(self, is_running):
        while is_running():
            self.input_queue.compute(self._publish)

    def _publish(self, message):
        chunk_trace, camera_trace, video_metadata = message
        camera_context = get_context(camera_trace)

        message = VideoChunkMessage(camera_id=video_metadata.camera_id,
                                    timestamp=video_metadata.timestamp,
                                    trace=chunk_trace,
                                    encoding=video_metadata.encoding,
                                    framerate=video_metadata.framerate,
                                    width=video_metadata.resolution[0],
                                    height=video_metadata.resolution[1])

        with self.tracer.start_as_current_span('store', context=camera_context):
            self.storage.store(name=str(message), filepath=video_metadata.filename)

        with self.tracer.start_as_current_span('publish', context=camera_context):
            self.publisher.publish(encode(message))

        with self.tracer.start_as_current_span('clean', context=camera_context):
            delete_video(video_metadata.filename)
