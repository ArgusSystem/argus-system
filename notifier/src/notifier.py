from utils.metadata.src.repository.sightings import get_sighting_for
#from .notification_history import NotificationHistory
from utils.metadata.src.repository.notifications import create_notification, get_wardens, get_offenders
from utils.events.src.messages.broken_restriction_message import BrokenRestrictionMessage
from utils.events.src.messages.marshalling import decode
from utils.tracing.src.tracer import get_context


def _notify(users, broken_restriction_id):
    for user_id in users:
        create_notification(user_id, broken_restriction_id)


class Notifier:

    def __init__(self, tracer):
        self.tracer = tracer
        #self.notification_history = NotificationHistory()

    def on_broken_rule(self, message):
        broken_restriction_message: BrokenRestrictionMessage = decode(BrokenRestrictionMessage, message)

        face_id = broken_restriction_message.face_id
        restriction_id = broken_restriction_message.restriction_id
        broken_restriction_id = broken_restriction_message.broken_restriction_id

        sighting = get_sighting_for(face_id, restriction_id)

        with self.tracer.start_as_current_span('notifier', context=get_context(broken_restriction_message.trace_id)):
            #history_entry = self.notification_history.update(sighting)

            if sighting.offender():
                _notify(get_offenders(sighting.offender()), broken_restriction_id)

            _notify(get_wardens(restriction_id), broken_restriction_id)
