from utils.events.src.messages.message_type import MessageType
from utils.events.src.messages.marshalling import decode
from utils.video_storage import StorageFactory
from .video_storage import VideoStorage
from .video_iterator import VideoIterator
from .frame_storage import FrameStorage


STORAGE_KEY = 'storage'
SAMPLING_KEY = 'sampling_rate'


class VideoProcessor:

    def __init__(self, configuration):
        storage_factory = StorageFactory(**configuration[STORAGE_KEY])
        self.video_chunks_storage = VideoStorage(storage_factory)
        self.frames_storage = FrameStorage(storage_factory)
        self.sampling_rate = configuration[SAMPLING_KEY]

    def process(self, message):
        video_chunk_message = decode(message, MessageType.VIDEO_CHUNK)
        video_filepath = self.video_chunks_storage.fetch_video(str(video_chunk_message))

        for offset, frame in VideoIterator(video_filepath):
            if offset % self.sampling_rate == 0:

                self.frames_storage.store()

