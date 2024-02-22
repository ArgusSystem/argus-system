from flask import jsonify, request

from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.marshalling import encode
from utils.events.src.messages.matched_face_message import MatchedFaceMessage
from utils.orm.src.database import db
from utils.orm.src.models import BrokenRestriction, Camera, Face, VideoChunk
from utils.tracing.src.tracer import get_trace_parent

TAG_AS_UNKNOWN = -1
TAG_DELETE_FACE = -2


def _get_faces(camera_id, person_id, start_time, end_time):
    return [{
        'id': known_face.id,
        'url': known_face.image_key()
    } for known_face in Face
        .select()
        .join(VideoChunk)
        .join(Camera)
        .where((Camera.id == camera_id) &
               (Face.person == person_id) &
               (Face.timestamp >= start_time) &
               (Face.timestamp <= end_time) &
               Face.is_match)
    ]


class KnownFacesController:

    def __init__(self, publisher_to_warden_configuration, tracer):
        self.publisher_to_warden = Publisher.new(**publisher_to_warden_configuration)
        self.tracer = tracer

    def make_routes(self, app):
        app.route('/known_faces/<camera_id>/<person_id>/<start_time>/<end_time>')(_get_faces)
        app.route('/known_faces/re_tag', methods=['POST'])(self._known_re_tag)

    def _known_re_tag(self):
        data = request.json
        person_id = data['person']
        faces = data['faces']

        if person_id != TAG_DELETE_FACE:
            # Update database
            with db.atomic():
                Face.update(person_id=Face.person if person_id == TAG_AS_UNKNOWN else person_id,
                            is_match=person_id != TAG_AS_UNKNOWN)\
                    .where(Face.id.in_(faces)) \
                    .execute()

                BrokenRestriction.delete() \
                    .where(BrokenRestriction.face.in_(faces)) \
                    .execute()

            # Send faces to warden
            with self.tracer.start_as_current_span(f'known-faces-re-tag'):
                trace = get_trace_parent()

                for face_id in faces:
                    with self.tracer.start_as_current_span(face_id):
                        self.publisher_to_warden.publish(encode(MatchedFaceMessage(face_id=face_id, trace=trace)))

        else:
            # Update database
            Face.delete().where(Face.id.in_(faces)).execute()

        return jsonify(success=True)
