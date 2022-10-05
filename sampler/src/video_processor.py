import os
import shutil
from logging import getLogger

from utils.events.src.message_clients.rabbitmq.publisher import Publisher
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.events.src.messages.marshalling import decode, encode
from utils.events.src.messages.frame_message import FrameMessage
from utils.tracing.src.tracer import get_tracer
from utils.video_storage import StorageFactory, StorageType

from .sample_video import sample
from .fetch_video_chunk import fetch
from .convert_to_video_stream import convert

logger = getLogger(__name__)


class VideoProcessor:

    def __init__(self, sampling_rate,
                 storage_configuration,
                 tracer_configuration,
                 frame_publisher_configuration,
                 video_chunk_publisher_configuration):
        self.sampling_rate = sampling_rate

        storage_factory = StorageFactory(**storage_configuration)
        self.video_chunk_storage = storage_factory.new(StorageType.VIDEO_CHUNKS)
        self.frame_storage = storage_factory.new(StorageType.VIDEO_FRAMES)

        self.frame_publisher = Publisher.new(**frame_publisher_configuration)
        self.video_chunk_publisher = Publisher.new(**video_chunk_publisher_configuration)
        self.tracer = get_tracer(**tracer_configuration)

    def process(self, message):
        video_chunk_message: VideoChunkMessage = decode(VideoChunkMessage, message)
        video_chunk_id = str(video_chunk_message)

        with self.tracer.start_as_current_span(video_chunk_id):
            with self.tracer.start_as_current_span('sampler'):
                with self.tracer.start_as_current_span('fetch'):
                    original_video_chunk = fetch(video_chunk_message, self.video_chunk_storage)

                with self.tracer.start_as_current_span('re-encode'):
                    converted_video_chunk = convert(original_video_chunk)

                with self.tracer.start_as_current_span('sample'):
                    frames_dir, frames = sample(converted_video_chunk, self.sampling_rate)

                with self.tracer.start_as_current_span('store-and-publish-frames'):
                    self._store_and_publish_frames(video_chunk_id=video_chunk_id, frames=frames)

                with self.tracer.start_as_current_span('store-and-publish-chunk'):
                    self._store_and_publish_video_chunk(video_chunk_id=video_chunk_id, video_chunk=converted_video_chunk)

                with self.tracer.start_as_current_span('clean'):
                    os.remove(original_video_chunk.filepath)
                    os.remove(converted_video_chunk.filepath)
                    shutil.rmtree(frames_dir)

        logger.info('Finished processing chunk %s', video_chunk_id)

    def _store_and_publish_frames(self, video_chunk_id, frames):
        for frame in frames:
            frame_message = FrameMessage(video_chunk_id, frame.offset)
            self.frame_storage.store(name=str(frame_message), filepath=frame.filepath)
            self.frame_publisher.publish(encode(frame_message))

    def _store_and_publish_video_chunk(self, video_chunk_id, video_chunk):
        self.video_chunk_storage.store(name=video_chunk_id, filepath=video_chunk.filepath)

        self.video_chunk_publisher.publish(encode(VideoChunkMessage(
            camera_id=video_chunk.camera_id,
            timestamp=video_chunk.timestamp,
            encoding=video_chunk.encoding,
            framerate=video_chunk.framerate,
            width=video_chunk.width,
            height=video_chunk.height,
            sampling_rate=self.sampling_rate
        )))
