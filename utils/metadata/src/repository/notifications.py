from peewee import JOIN

from utils.orm.src.models import BrokenRestriction, \
    Camera, \
    Face, \
    Notification, \
    Person, \
    Restriction, \
    RestrictionSeverity, \
    RestrictionWarden, \
    User, \
    UserPerson, \
    VideoChunk


# TODO: Fix with new Restriction

def create_notification(user_id, broken_restriction_id):
    Notification(user=user_id, broken_restriction_id=broken_restriction_id).save()


def get_offenders(offender_id):
    return map(lambda user_person: user_person.user_id, UserPerson
               .select(UserPerson.user_id)
               .where(UserPerson.person == offender_id)
               .execute())


def get_wardens(restriction_id):
    return map(lambda user_person: user_person.user_id, UserPerson
               .select(UserPerson.user_id)
               .join(Person, on=(Person.id == UserPerson.person_id))
               .join(RestrictionWarden, on=(RestrictionWarden.role_id == Person.role_id))
               .join(Restriction, on=(Restriction.id == RestrictionWarden.restriction_id))
               .where(Restriction.id == restriction_id)
               .distinct()
               .execute())


def _join_metadata(query):
    return query \
        .join(BrokenRestriction, on=(Notification.broken_restriction_id == BrokenRestriction.id)) \
        .join(Face, on=(BrokenRestriction.face_id == Face.id)) \
        .join(VideoChunk, on=(Face.video_chunk_id == VideoChunk.id)) \
        .join(Camera, on=(VideoChunk.camera_id == Camera.id)) \
        .join(Person, JOIN.LEFT_OUTER, on=(Face.person_id == Person.id)) \
        .join(Restriction, on=(BrokenRestriction.restriction_id == Restriction.id)) \
        .join(RestrictionSeverity, on=(Restriction.severity_id == RestrictionSeverity.id))


def get_notification(notification_id):
    return _join_metadata(Notification
                          .select(Notification, BrokenRestriction, Face, Person, Restriction)) \
        .where(Notification.id == notification_id) \
        .get()


def get_notifications(username, count):
    return _join_metadata(Notification
                          .select(Notification, User, BrokenRestriction, Face, Person, Restriction, RestrictionSeverity)
                          .join(User)) \
        .where(User.username == username) \
        .order_by(Face.timestamp.desc()) \
        .limit(count)


def count_notifications(username):
    return Notification.select() \
        .join(User) \
        .where((User.username == username) & (~Notification.read)) \
        .count()


def mark_notification_read(notification_id):
    Notification \
        .update(read=True) \
        .where(Notification.id == notification_id) \
        .execute()
