import os
from logging import getLogger

from utils.events.src.message_clients.rabbitmq.publisher import Publisher
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.events.src.messages.marshalling import decode, encode
from utils.events.src.messages.frame_message import FrameMessage
from utils.video_storage import StorageFactory
from .video_storage import VideoStorage
from .video_iterator import VideoIterator
from .frame_storage import FrameStorage
from .video_writer import VideoWriter


class VideoProcessor:

    def __init__(self, sampling_rate, storage_configuration,
                 frame_publisher_configuration,
                 video_chunk_publisher_configuration):
        storage_factory = StorageFactory(**storage_configuration)
        self.video_chunks_storage = VideoStorage(storage_factory)
        self.frames_storage = FrameStorage(storage_factory)
        self.frame_publisher = Publisher.new(**frame_publisher_configuration)
        self.video_chunk_publisher = Publisher.new(**video_chunk_publisher_configuration)
        self.sampling_rate = sampling_rate
        self.logger = getLogger(__name__)

    def process(self, message):
        video_chunk_message: VideoChunkMessage = decode(VideoChunkMessage, message)
        video_chunk_id = str(video_chunk_message)
        self.logger.info('Starting processing: %s', video_chunk_id)
        video_filepath = self.video_chunks_storage.fetch(video_chunk_id, video_chunk_message.encoding)

        # Rewrite video with new encoding
        video_writer = VideoWriter(camera=video_chunk_message.camera_id,
                                   timestamp=video_chunk_message.timestamp,
                                   framerate=video_chunk_message.framerate,
                                   width=video_chunk_message.width,
                                   height=video_chunk_message.height)

        # Iterate through frames
        for offset, frame in VideoIterator(video_filepath):
            # Send frame event for processing
            if offset % self.sampling_rate == 0:
                self._sample_frame(frame, offset, video_chunk_id)

            video_writer.write(frame)

        video_writer.close()

        # Upload video with new encoding
        self.video_chunks_storage.store(video_chunk_id, video_writer.filename)

        video_chunk_message.sampling_rate = self.sampling_rate
        self.video_chunk_publisher.publish(encode(video_chunk_message))

        # Delete local videos
        os.remove(video_filepath)
        os.remove(video_writer.filename)

        self.logger.info('Finished processing: %s', video_chunk_id)

    def _sample_frame(self, frame, offset, video_chunk):
        frame_message = FrameMessage(video_chunk, offset)

        self.frames_storage.store(name=str(frame_message), frame=frame)
        self.frame_publisher.publish(encode(frame_message))
