from .message_type import MessageType


class VideoChunkMessage:

    def __init__(self, camera_id, timestamp):
        self.mtype = MessageType.VIDEO_CHUNK
        self.camera_id = camera_id
        self.timestamp = timestamp

    def to_json(self):
        return {
            'camera_id': self.camera_id,
            'timestamp': self.timestamp
        }

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.camera_id == other.camera_id and self.timestamp == other.timestamp

        return False
