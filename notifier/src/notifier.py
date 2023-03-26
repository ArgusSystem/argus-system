from utils.events.src.messages.broken_restriction_message import BrokenRestrictionMessage
from utils.events.src.messages.marshalling import decode
from utils.orm.src.models import Notification, Person, Restriction, RestrictionWarden, UserPerson
from utils.tracing.src.tracer import get_context


def _create_notification(user_id, broken_restriction_id):
    Notification(user=user_id, broken_restriction_id=broken_restriction_id).save()


def _get_offenders(offender_id):
    return map(lambda user_person: user_person.user_id, UserPerson
               .select(UserPerson.user_id)
               .where(UserPerson.person == offender_id)
               .execute())


def _get_wardens(restriction_id):
    return map(lambda user_person: user_person.user_id, UserPerson
               .select(UserPerson.user_id)
               .join(Person, on=(Person.id == UserPerson.person_id))
               .join(RestrictionWarden, on=(RestrictionWarden.role_id == Person.role_id))
               .join(Restriction, on=(Restriction.id == RestrictionWarden.restriction_id))
               .where(Restriction.id == restriction_id)
               .distinct()
               .execute())


class Notifier:

    def __init__(self, tracer):
        self.tracer = tracer

    # TODO: Watch out for too many notifications, use sightings to check if already checked
    def on_broken_rule(self, message):
        broken_restriction_message: BrokenRestrictionMessage = decode(BrokenRestrictionMessage, message)

        with self.tracer.start_as_current_span('notifier', context=get_context(broken_restriction_message.trace_id)):
            for user_id in _get_offenders(broken_restriction_message.face_id):
                _create_notification(user_id, broken_restriction_message.broken_restriction_id)

            for user_id in _get_wardens(broken_restriction_message.restriction_id):
                _create_notification(user_id, broken_restriction_message.broken_restriction_id)
