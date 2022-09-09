from enum import Enum
from .video_chunk_message import VideoChunkMessage

class MessageType(Enum):
    VIDEO_CHUNK = ('video_chunk', VideoChunkMessage)

    def __init__(self, id, message_class):
        self.id = id
        self.message_class = message_class
