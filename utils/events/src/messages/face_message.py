from utils.image_processing.src.image_serialization import image_to_bytestring, bytestring_to_image


class FaceMessage:

    def __init__(self, video_chunk_id, face_id, cropped_face_bytestring):
        self.video_chunk_id = video_chunk_id
        self.face_id = face_id
        self.cropped_face = bytestring_to_image(cropped_face_bytestring)

    def to_json(self):
        return {
            'video_chunk_id': self.video_chunk_id,
            'face_id': self.face_id,
            'cropped_face_bytestring': image_to_bytestring(self.cropped_face),
        }

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.video_chunk_id == other.video_chunk_id and self.face_id == other.face_id

        return False
