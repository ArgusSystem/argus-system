from peewee import JOIN

from utils.orm.src.models import BrokenRestriction, Face, Notification, Person, Restriction, User


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


# TODO: Add time of notification using sighting information
def _get_notifications(username):
    notifications_query = Notification.select() \
        .join(User) \
        .join(BrokenRestriction, on=(Notification.broken_restriction_id == BrokenRestriction.id)) \
        .join(Face, on=(BrokenRestriction.face_id == Face.id)) \
        .join(Person, JOIN.LEFT_OUTER, on=(Face.person_id == Person.id)) \
        .join(Restriction, on=(BrokenRestriction.restriction_id == Restriction.id)) \
        .where(User.username == username)

    return list(map(_format_notifications, notifications_query))


class NotificationsController:

    @staticmethod
    def make_routes(app):
        app.route('/notifications/<username>')(_get_notifications)
