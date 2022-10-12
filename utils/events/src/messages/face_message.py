class FaceMessage:

    def __init__(self, video_chunk_id, offset, face_num, bounding_box, trace):
        self.video_chunk_id = video_chunk_id
        self.offset = offset
        self.face_num = face_num
        self.bounding_box = bounding_box
        self.trace = trace

    def to_json(self):
        return {
            'video_chunk_id': self.video_chunk_id,
            'offset': self.offset,
            'face_num': self.face_num,
            'bounding_box': self.bounding_box,
            'trace': self.trace
        }

    def __str__(self):
        return f'{self.video_chunk_id}-{self.offset}-{self.face_num}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.video_chunk_id == other.video_chunk_id and self.offset == other.offset \
                   and self.face_num == other.face_num

        return False
