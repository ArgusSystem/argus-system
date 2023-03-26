from flask import request
from peewee import JOIN

from utils.orm.src.models import AreaType, BrokenRestriction, Face, Notification, Person, Restriction, User


def _format_notifications(notification):
    return {
        'id': notification.id,
        'read': notification.read,
        'person': notification.broken_restriction.face.person.name,
        'restriction': {
            'area_type': notification.broken_restriction.restriction.area_type.name,
            'severity': notification.broken_restriction.restriction.severity
        }
    }


def _count_notifications(username):
    count = Notification.select().join(User).where((User.username == username) & (Notification.read == False)).count()
    return str(count)


# TODO: Add time of notification using sighting information
def _get_notifications(username):
    notifications_count = request.args.get('count')
    assert notifications_count

    notifications_query = Notification \
        .select(Notification, User, BrokenRestriction, Face, Person, Restriction, AreaType) \
        .join(User) \
        .join(BrokenRestriction, on=(Notification.broken_restriction_id == BrokenRestriction.id)) \
        .join(Face, on=(BrokenRestriction.face_id == Face.id)) \
        .join(Person, JOIN.LEFT_OUTER, on=(Face.person_id == Person.id)) \
        .join(Restriction, on=(BrokenRestriction.restriction_id == Restriction.id)) \
        .join(AreaType, on=(Restriction.area_type_id == AreaType.id)) \
        .where(User.username == username) \
        .limit(notifications_count)

    return list(map(_format_notifications, notifications_query))


class NotificationsController:

    @staticmethod
    def make_routes(app):
        app.route('/notifications/<username>')(_get_notifications)
        app.route('/notifications/<username>/count')(_count_notifications)
