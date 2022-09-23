from enum import Enum


class MessageType(Enum):
    VIDEO_CHUNK = 'video_chunk'
    FRAME = 'frame'
    FACE = 'face'
