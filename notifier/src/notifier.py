from .notification_history import NotificationHistory
from utils.metadata.src.repository.notifications import create_notification, get_wardens, get_offenders
from utils.events.src.messages.broken_restriction_message import BrokenRestrictionMessage
from utils.events.src.messages.marshalling import decode
from utils.tracing.src.tracer import get_context


class Notifier:

    def __init__(self, tracer):
        self.tracer = tracer
        self.notification_history = NotificationHistory()

    def on_broken_rule(self, message):
        broken_restriction_message: BrokenRestrictionMessage = decode(BrokenRestrictionMessage, message)

        face_id = broken_restriction_message.face_id
        restriction_id = broken_restriction_message.restriction_id
        broken_restriction_id = broken_restriction_message.broken_restriction_id

        with self.tracer.start_as_current_span('notifier', context=get_context(broken_restriction_message.trace_id)):
            self.notification_history.update(face_id, restriction_id)

            self._notify(get_offenders(face_id), face_id, restriction_id, broken_restriction_id)
            self._notify(get_wardens(restriction_id), face_id, restriction_id, broken_restriction_id)

    def _notify(self, users, face_id, restriction_id, broken_restriction_id):
        for user_id in users:
            if self.notification_history.should_notify(user_id, face_id, restriction_id):
                create_notification(user_id, broken_restriction_id)
                self.notification_history.mark_notification(user_id, face_id, restriction_id)
