from flask import jsonify, request

from utils.metadata.src.repository.notifications import count_notifications, get_notification, get_notification_faces, \
    get_notifications, \
    mark_notifications_read

UNKNOWN = 'UNKNOWN'


def _format_notification(n):
    return {
        'user_id': n.user.id,
        'read': n.read,
        'person_id': -1 if n.is_unknown else n.person.id,
        'person': UNKNOWN if n.is_unknown else n.person.name,
        'start_time': n.start_time,
        'end_time': n.end_time,
        'camera_id': n.camera.id,
        'place': n.camera.alias,
        'restriction_id': n.restriction.id,
        'restriction': {
            'rule': n.restriction.rule,
            'severity': n.restriction.severity.value
        }
    }


def _count_notifications(username):
    return str(count_notifications(username))


def _get_notification(username, camera_id, person_id, restriction_id, start_time):
    return _format_notification(get_notification(username, camera_id, person_id, restriction_id, start_time))


def _get_notifications(username):
    notifications_count = request.args.get('count')
    assert notifications_count

    return list(map(_format_notification, get_notifications(username, notifications_count)))


def _mark_notification_read(username, camera_id, person_id, restriction_id, start_time):
    mark_notifications_read(username, camera_id, person_id, restriction_id, start_time)
    return jsonify(success=True)


def _get_notification_faces(username, camera_id, person_id, restriction_id, start_time):
    faces = get_notification_faces(username, camera_id, person_id, restriction_id, start_time)

    return [{
        'id': face.id,
        'timestamp': face.timestamp,
        'image_key': face.image_key()
    } for face in faces]


class NotificationsController:

    @staticmethod
    def make_routes(app):
        app.route('/notifications/id/<username>/<camera_id>/<person_id>/<restriction_id>/<start_time>')(_get_notification)
        app.route('/notifications/id/<username>/<camera_id>/<person_id>/<restriction_id>/<start_time>/read', methods=['POST'])(_mark_notification_read)
        app.route('/notifications/id/<username>/<camera_id>/<person_id>/<restriction_id>/<start_time>/faces')(_get_notification_faces)
        app.route('/notifications/user/<username>')(_get_notifications)
        app.route('/notifications/user/<username>/count')(_count_notifications)
