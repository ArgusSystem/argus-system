from utils.image_processing.src.image_serialization import image_to_bytestring, bytestring_to_image


class FrameMessage:

    def __init__(self, video_chunk_id, frame_id, payload_bytestring):
        self.video_chunk_id = video_chunk_id
        self.frame_id = frame_id
        self.payload = bytestring_to_image(payload_bytestring)

    def to_json(self):
        return {
            'video_chunk_id': self.video_chunk_id,
            'frame_id': self.frame_id,
            'payload_bytestring': image_to_bytestring(self.payload),
        }

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.video_chunk_id == other.video_chunk_id and self.frame_id == other.frame_id

        return False
