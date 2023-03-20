class BrokenRuleMessage:

    def __init__(self, face_id, restriction_id):
        self.face_id = face_id
        self.restriction_id = restriction_id

    def to_json(self):
        return {
            'face_id': self.face_id,
            'restriction_id': self.restriction_id
        }

    def __str__(self):
        return f'{self.face_id}-{self.restriction_id}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.face_id == other.face_id and self.restriction_id == other.restriction_id

        return False
