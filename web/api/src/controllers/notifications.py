from flask import request

from utils.metadata.src.repository.notifications import count_notifications, get_notification, get_notifications


def _format_notification(notification):
    return {
        'id': notification.id,
        'read': notification.read,
        'person': notification.broken_restriction.face.person.name,
        'timestamp': notification.broken_restriction.face.timestamp,
        'place': notification.broken_restriction.face.video_chunk.camera.alias,
        'restriction': {
            'area_type': notification.broken_restriction.restriction.area_type.name,
            'severity': notification.broken_restriction.restriction.severity
        }
    }


def _count_notifications(username):
    return str(count_notifications(username))


def _get_notification(notification_id):
    return _format_notification(get_notification(notification_id))


def _get_notifications(username):
    notifications_count = request.args.get('count')
    assert notifications_count

    return list(map(_format_notification, get_notifications(username, notifications_count)))


class NotificationsController:

    @staticmethod
    def make_routes(app):
        app.route('/notifications/id/<notification_id>')(_get_notification)
        app.route('/notifications/user/<username>')(_get_notifications)
        app.route('/notifications/user/<username>/count')(_count_notifications)
