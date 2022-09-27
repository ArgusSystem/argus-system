from utils.image_processing.src.image_serialization import image_to_bytestring, bytestring_to_image


class FaceMessage:

    def __init__(self, video_chunk_id, face_id):
        self.video_chunk_id = video_chunk_id
        self.face_id = face_id

    def to_json(self):
        return {
            'video_chunk_id': self.video_chunk_id,
            'face_id': self.face_id
        }

    def __str__(self):
        return f'{self.video_chunk_id}-{self.face_id}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.video_chunk_id == other.video_chunk_id and self.face_id == other.face_id

        return False
