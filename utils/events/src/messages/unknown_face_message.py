class UnknownFaceMessage:

    def __init__(self, face_id, embedding, trace):
        self.face_id = face_id
        self.embedding = embedding
        self.trace = trace

    def to_json(self):
        return {
            'face_id': self.face_id,
            'embedding': self.embedding,
            'trace': self.trace
        }

    def __str__(self):
        return f'{self.face_id}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.face_id == other.face_id

        return False
