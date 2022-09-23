from utils.events.src.message_clients.rabbitmq.publisher import Publisher
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.events.src.messages.marshalling import decode, encode
from utils.events.src.messages.frame_message import FrameMessage
from utils.video_storage import StorageFactory
from .video_storage import VideoStorage
from .video_iterator import VideoIterator
from .frame_storage import FrameStorage
from .video_writer import VideoWriter
import os


class VideoProcessor:

    def __init__(self, sampling_rate,storage_configuration, publisher_configuration):
        storage_factory = StorageFactory(**storage_configuration)
        self.video_chunks_storage = VideoStorage(storage_factory)
        self.frames_storage = FrameStorage(storage_factory)
        self.publisher = Publisher.new(**publisher_configuration)
        self.sampling_rate = sampling_rate

    def process(self, message):
        video_chunk_message = decode(VideoChunkMessage, message)
        video_chunk_id = str(video_chunk_message)
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
        # TODO: publish for webserver
        self.publisher.publish()

        # Delete local videos
        os.remove(video_filepath)
        os.remove(video_writer.filename)

    def _sample_frame(self, frame, offset, video_chunk):
        frame_message = FrameMessage(video_chunk, offset)

        self.frames_storage.store(name=str(frame_message), frame=frame)
        self.publisher.publish(encode(frame_message))
