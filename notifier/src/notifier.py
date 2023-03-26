from utils.events.src.messages.broken_rule_message import BrokenRestrictionMessage
from utils.events.src.messages.marshalling import decode
from utils.orm.src.models import Notification, PersonRole, Restriction, RestrictionWarden, UserPerson
from utils.orm.src.models.restriction_warden import RestrictionWarden
from utils.tracing.src.tracer import get_context


def _create_notification(user, broken_restriction_id):
    Notification(user=user, broken_restriction_id=broken_restriction_id).save()


def _get_offenders(offender_id):
    return UserPerson \
        .select(UserPerson.user) \
        .where(UserPerson.person == offender_id) \
        .get()


def _get_wardens(broken_restriction_id):
    return UserPerson \
        .select(UserPerson.user) \
        .join(PersonRole)\
        .join(RestrictionWarden, on=(PersonRole.id == RestrictionWarden.role_id))\
        .join(Restriction, on=(RestrictionWarden.restriction_id == Restriction.id)) \
        .where(Restriction.id == broken_restriction_id) \
        .distinct() \
        .get()


class Notifier:

    def __init__(self, tracer):
        self.tracer = tracer

    # TODO: Watch out for too many notifications, use sightings to check if already checked
    def on_broken_rule(self, message):
        broken_restriction_message: BrokenRestrictionMessage = decode(BrokenRestrictionMessage, message)

        with self.tracer.start_as_current_span('notifier', context=get_context(broken_restriction_message.trace_id)):
            for user in _get_offenders(broken_restriction_message.face_id):
                _create_notification(user, broken_restriction_message.broken_restriction_id)

            for user in _get_wardens(broken_restriction_message.broken_restriction_id):
                _create_notification(user, broken_restriction_message.broken_restriction_id)
