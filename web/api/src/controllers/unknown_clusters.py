from flask import jsonify, request
from peewee import IntegrityError, fn

from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.marshalling import encode
from utils.events.src.messages.matched_face_message import MatchedFaceMessage
from utils.orm.src.database import db
from utils.orm.src.models import Camera, Face, VideoChunk, UnknownCluster, UnknownFace
from utils.tracing.src.tracer import get_trace_parent, set_span_in_context


def _get_unknown_clusters():
    clusters_count = request.args.get('count')
    assert clusters_count

    faces_count = fn.COUNT(UnknownFace.face_id)

    return [{
        'id': face.cluster_id,
        'faces_count': face.faces_count
    } for face in UnknownFace
    .select(UnknownFace.cluster_id, faces_count.alias('faces_count'))
    .group_by(UnknownFace.cluster_id)
    .order_by(faces_count.desc())
    .limit(clusters_count)]


def _get_cluster_faces(cluster_id):
    return [{
        'id': unknown_face.face.id,
        'camera': unknown_face.face.video_chunk.camera.alias,
        'timestamp': unknown_face.face.video_chunk.timestamp,
        'url': '-'.join([unknown_face.face.video_chunk.camera.alias,
                         str(unknown_face.face.video_chunk.timestamp),
                         str(unknown_face.face.offset),
                         str(unknown_face.face.face_num)])
    } for unknown_face in UnknownFace
    .select(Face.id, Face.offset, Face.face_num, VideoChunk.timestamp, Camera.alias)
    .join(UnknownCluster)
    .switch(UnknownFace)
    .join(Face)
    .join(VideoChunk)
    .join(Camera)
    .where(UnknownCluster.id == cluster_id)]


class UnknownClustersController:

    def __init__(self, publisher_configuration, tracer):
        self.publisher = Publisher.new(**publisher_configuration)
        self.tracer = tracer

    def make_routes(self, app):
        app.route('/unknown_clusters')(_get_unknown_clusters)
        app.route('/unknown_clusters/<cluster_id>/faces')(_get_cluster_faces)
        app.route('/unknown_clusters/<cluster_id>/re_tag', methods=['POST'])(self._re_tag)

    def _re_tag(self, cluster_id):
        data = request.json

        # Update database
        with db.transaction() as txn:
            Face.update(person_id=data['person']) \
                .where(Face.id.in_(data['faces'])) \
                .execute()

            UnknownFace.delete() \
                .where(UnknownFace.face_id.in_(data['faces'])) \
                .execute()

            txn.commit()

            try:
                UnknownCluster.delete() \
                    .where(UnknownCluster.id == cluster_id) \
                    .execute()
            except IntegrityError:
                txn.rollback()

        # Send faces to warden
        with self.tracer.start_as_current_span(f'cluster-{cluster_id}-re-tag'):
            trace = get_trace_parent()

            for face_id in data['faces']:
                with self.tracer.start_as_current_span(face_id):
                    self.publisher.publish(encode(MatchedFaceMessage(face_id=face_id, trace=trace)))

        return jsonify(success=True)
