from enum import Enum


class StorageType(Enum):
    VIDEO_CHUNKS = 'video-chunks'
    VIDEO_FRAMES = 'video-frames'
    FRAME_FACES = 'frame-faces'
    PEOPLE = 'people'
