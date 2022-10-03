import os
import shutil
from logging import getLogger

from utils.events.src.message_clients.rabbitmq.publisher import Publisher
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.events.src.messages.marshalling import decode, encode
from utils.events.src.messages.frame_message import FrameMessage
from utils.video_storage import StorageFactory, StorageType

from .sample_video import sample
from .fetch_video_chunk import fetch
from .convert_to_video_stream import convert


class VideoProcessor:

    def __init__(self, sampling_rate, storage_configuration,
                 frame_publisher_configuration,
                 video_chunk_publisher_configuration):
        self.logger = getLogger(__name__)
        self.sampling_rate = sampling_rate

        storage_factory = StorageFactory(**storage_configuration)
        self.video_chunk_storage = storage_factory.new(StorageType.VIDEO_CHUNKS)
        self.frame_storage = storage_factory.new(StorageType.VIDEO_FRAMES)

        self.frame_publisher = Publisher.new(**frame_publisher_configuration)
        self.video_chunk_publisher = Publisher.new(**video_chunk_publisher_configuration)

    def process(self, message):
        video_chunk_message: VideoChunkMessage = decode(VideoChunkMessage, message)
        video_chunk_id = str(video_chunk_message)

        self.logger.info('Starting processing: %s', video_chunk_id)

        original_video_chunk = fetch(video_chunk_message, self.video_chunk_storage)
        frames_dir, frames = sample(original_video_chunk, self.sampling_rate)

        for frame in frames:
            frame_message = FrameMessage(video_chunk_id, frame.offset)
            self.frame_storage.store(name=str(frame_message), filepath=frame.filepath)
            self.frame_publisher.publish(encode(frame_message))

        converted_video_chunk = convert(original_video_chunk)

        # Upload video with new encoding
        self.video_chunk_storage.store(name=video_chunk_id, filepath=converted_video_chunk.filepath)
        # Publish video for stream
        self.video_chunk_publisher.publish(encode(VideoChunkMessage(
            camera_id=converted_video_chunk.camera_id,
            timestamp=converted_video_chunk.timestamp,
            encoding=converted_video_chunk.encoding,
            framerate=converted_video_chunk.framerate,
            width=converted_video_chunk.width,
            height=converted_video_chunk.height,
            sampling_rate=self.sampling_rate
        )))

        # Delete local videos
        os.remove(original_video_chunk.filepath)
        os.remove(converted_video_chunk.filepath)
        shutil.rmtree(frames_dir)

        self.logger.info('Finished processing: %s', video_chunk_id)
