class BrokenRestrictionMessage:

    def __init__(self, broken_restriction_id, face_id, restriction_id, trace_id):
        self.broken_restriction_id = broken_restriction_id
        self.face_id = face_id
        self.restriction_id = restriction_id
        self.trace_id = trace_id

    def to_json(self):
        return {
            'broken_restriction_id': self.broken_restriction_id,
            'face_id': self.face_id,
            'restriction_id': self.restriction_id,
            'trace_id': self.trace_id
        }
