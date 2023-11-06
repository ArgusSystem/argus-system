from logging import getLogger

from .local_video import delete_video
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.marshalling import encode
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.tracing.src.tracer import get_trace_parent
from utils.video_storage import StorageFactory, StorageType

logger = getLogger(__name__)


class VideoPublisher:

    def __init__(self, input_queue, tracer, camera_id, publisher_configuration, storage_configuration):
        self.input_queue = input_queue
        self.tracer = tracer
        self.camera_id = camera_id
        self.publisher = Publisher.new(**publisher_configuration)
        self.storage = StorageFactory(**storage_configuration).new(StorageType.VIDEO_CHUNKS)

    def publish(self, is_running):
        while is_running():
            self.input_queue.compute(self._publish)

    def _publish(self, processing_chunk):
        video_metadata = processing_chunk.metadata
        context = processing_chunk.context

        message = VideoChunkMessage(camera_id=self.camera_id,
                                    timestamp=video_metadata.timestamp,
                                    trace=get_trace_parent(context),
                                    encoding=video_metadata.encoding,
                                    duration=video_metadata.duration,
                                    sequence_id=video_metadata.sequence_id)

        with self.tracer.start_as_current_span('store', context=context):
            self.storage.store(name=str(message), filepath=video_metadata.filename)

        with self.tracer.start_as_current_span('publish', context=context):
            self.publisher.publish(encode(message))

        with self.tracer.start_as_current_span('clean', context=context):
            delete_video(video_metadata.filename)

        logger.info('Recorded: %s', video_metadata.timestamp)

        processing_chunk.span.end()
