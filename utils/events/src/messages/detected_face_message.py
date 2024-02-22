
class DetectedFaceMessage:

    def __init__(self, video_chunk_id, offset, timestamp, face_num, name, role, person_id, bounding_box, probability, is_match, trace):
        self.video_chunk_id = video_chunk_id
        self.offset = offset
        self.timestamp = timestamp
        self.face_num = face_num
        self.name = name
        self.role = role
        self.person_id = person_id
        self.bounding_box = bounding_box
        self.probability = probability
        self.is_match = is_match
        self.trace = trace

    def to_json(self):
        return {
            'video_chunk_id': self.video_chunk_id,
            'offset': self.offset,
            'timestamp': self.timestamp,
            'face_num': self.face_num,
            'name': self.name,
            'role': self.role,
            'person_id': self.person_id,
            'bounding_box': self.bounding_box,
            'probability': self.probability,
            'is_match': self.is_match,
            'trace': self.trace
        }

    def __str__(self):
        return f'{self.video_chunk_id}-{self.offset}-{self.face_num}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.video_chunk_id == other.video_chunk_id and self.offset == other.offset \
                   and self.face_num == other.face_num

        return False
