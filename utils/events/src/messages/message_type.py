from enum import Enum


class MessageType(Enum):
    VIDEO_CHUNK = 'video_chunk'
    VIDEO_FRAME = 'video_frame'
