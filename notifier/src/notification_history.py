class NotificationHistory:

    def __init__(self):
        self.history = {}

    def update(self, face_id, restriction_id):
        return False

    def should_notify(self, user_id, face_id, restriction_id):
        return False

    def mark_notification(self, user_id, face_id, restriction_id):
        return
