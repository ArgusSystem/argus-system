from peewee import JOIN

from utils.metadata.src.repository.sightings import get_sighting_for
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
from utils.orm.src.views import NotificationSummary


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
        .join(Camera, on=(NotificationSummary.camera == Camera.id)) \
        .join(Restriction, on=(NotificationSummary.restriction == Restriction.id)) \
        .join(Person, JOIN.LEFT_OUTER, on=(NotificationSummary.person == Person.id))


def get_notification(user_id, camera_id, person_id, restriction_id, start_time):
    return _join_metadata(NotificationSummary
                          .select(NotificationSummary.user, NotificationSummary.camera,
                                  NotificationSummary.person, NotificationSummary.is_unknown,
                                  NotificationSummary.restriction, NotificationSummary.severity,
                                  NotificationSummary.start_time, NotificationSummary.end_time,
                                  NotificationSummary.read, NotificationSummary.notification_ids)) \
        .where((NotificationSummary.user == user_id) &
               (NotificationSummary.camera == camera_id) &
               (NotificationSummary.person == person_id) &
               (NotificationSummary.restriction == restriction_id) &
               (NotificationSummary.start_time <= start_time) &
               (NotificationSummary.end_time >= start_time)) \
        .get()


def get_notifications(username, count):
    return _join_metadata(NotificationSummary
                          .select(NotificationSummary.user, NotificationSummary.camera,
                                  NotificationSummary.person, NotificationSummary.is_unknown,
                                  NotificationSummary.restriction, NotificationSummary.severity,
                                  NotificationSummary.start_time, NotificationSummary.end_time,
                                  NotificationSummary.read, NotificationSummary.notification_ids)
                          .join(User, on=(NotificationSummary.user == User.id))) \
        .where(User.username == username) \
        .order_by(NotificationSummary.start_time.desc()) \
        .limit(count)


def count_notifications(username):
    return NotificationSummary.select() \
        .join(User, on=(NotificationSummary.user == User.id)) \
        .where((User.username == username) & (~NotificationSummary.read)) \
        .count()


def mark_notifications_read(user_id, camera_id, person_id, restriction_id, start_time):
    notification_summary = get_notification(user_id, camera_id, person_id, restriction_id, start_time)

    Notification \
        .update(read=True) \
        .where(Notification.id.in_(notification_summary.notification_ids)) \
        .execute()


def get_notification_faces(user_id, camera_id, person_id, restriction_id, start_time):
    notification_summary = get_notification(user_id, camera_id, person_id, restriction_id, start_time)

    notifications = (Notification.select(Notification, BrokenRestriction, Face)
                     .join(BrokenRestriction)
                     .join(Face)
                     .where(Notification.id.in_(notification_summary.notification_ids)))

    return [n.broken_restriction.face for n in notifications]
