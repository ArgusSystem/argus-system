from flask import jsonify, request

from utils.metadata.src.repository.notifications import count_notifications, get_notification, get_notifications, \
    mark_notification_read

UNKNOWN = 'UNKNOWN'


def _format_notification(notification):
    face = notification.broken_restriction.face

    return {
        'id': notification.id,
        'read': notification.read,
        'person': face.person.name if face.is_match else UNKNOWN,
        'timestamp': face.timestamp,
        'place': face.video_chunk.camera.alias,
        'restriction': {
            'rule': notification.broken_restriction.restriction.rule,
            'severity': notification.broken_restriction.restriction.severity.value
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


def _mark_notification_read(notification_id):
    mark_notification_read(notification_id)
    return jsonify(success=True)


class NotificationsController:

    @staticmethod
    def make_routes(app):
        app.route('/notifications/id/<notification_id>')(_get_notification)
        app.route('/notifications/id/<notification_id>/read', methods=['POST'])(_mark_notification_read)
        app.route('/notifications/user/<username>')(_get_notifications)
        app.route('/notifications/user/<username>/count')(_count_notifications)
