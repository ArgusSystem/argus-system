import numpy as np
from flask import jsonify, request
from peewee import IntegrityError, JOIN, fn

from clusterer.src.cluster_storage import ClusterStorage
from clusterer.src.clustering import fit
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.marshalling import encode
from utils.events.src.messages.matched_face_message import MatchedFaceMessage
from utils.events.src.messages.unknown_face_message import UnknownFaceMessage
from utils.orm.src.database import db
from utils.orm.src.models import Camera, Face, VideoChunk, UnknownCluster, UnknownFace, BrokenRestriction
from utils.tracing.src.tracer import get_trace_parent

TAG_DELETE_FACE = -2


def _get_unknown_clusters():
    clusters_count = request.args.get('count')
    assert clusters_count

    faces_count = fn.COUNT(UnknownFace.face_id)

    return [{
        'id': face.cluster.id,
        'faces_count': face.faces_count,
        'outliers': face.cluster.outliers
    } for face in UnknownFace
        .select(UnknownCluster.id, faces_count.alias('faces_count'), UnknownCluster.outliers)
        .join(UnknownCluster)
        .group_by(UnknownCluster.id, UnknownCluster.outliers)
        .order_by(faces_count.desc())
        .limit(clusters_count)]


def _get_cluster_faces(cluster_id):
    return [{
        'id': unknown_face.face.id,
        'camera': unknown_face.face.video_chunk.camera.alias,
        'timestamp': unknown_face.face.video_chunk.timestamp,
        'url': unknown_face.face.image_key()
    } for unknown_face in UnknownFace
    .select(Face.id, Face.offset, Face.face_num, VideoChunk.timestamp, Camera.alias)
    .join(UnknownCluster)
    .switch(UnknownFace)
    .join(Face)
    .join(VideoChunk)
    .join(Camera)
    .where(UnknownCluster.id == cluster_id)]


def _fit():
    faces = (Face.select()
             .join(UnknownFace, JOIN.LEFT_OUTER)
             .where((~Face.is_match) & (UnknownFace.cluster.is_null())))

    embeddings = np.array([face.embedding for face in faces])

    clt = fit(embeddings)

    cluster_storage = ClusterStorage(False)

    for face, label in zip(map(lambda f: f.id, faces), clt.labels_):
        cluster_storage.store(face, label)

    return jsonify(success=True)


def safe_delete_cluster(transaction, cluster_id):
    try:
        UnknownCluster.delete() \
            .where(UnknownCluster.id == cluster_id) \
            .execute()
    except IntegrityError:
        transaction.rollback()


class UnknownClustersController:

    def __init__(self, publisher_to_warden_configuration, tracer):
        self.publisher_to_warden = Publisher.new(**publisher_to_warden_configuration)
        self.tracer = tracer

    def make_routes(self, app):
        app.route('/unknown_clusters')(_get_unknown_clusters)
        app.route('/unknown_clusters/fit', methods=['POST'])(_fit)
        app.route('/unknown_clusters/<cluster_id>/faces')(_get_cluster_faces)
        app.route('/unknown_clusters/<cluster_id>/re_tag', methods=['POST'])(self._re_tag)

    def _re_tag(self, cluster_id):
        data = request.json
        person_id = data['person']
        faces = data['faces']

        if person_id != TAG_DELETE_FACE:
            # Update database
            with db.transaction() as txn:
                Face.update(person_id=person_id, is_match=True) \
                    .where(Face.id.in_(faces)) \
                    .execute()
                UnknownFace.delete() \
                    .where(UnknownFace.face_id.in_(faces)) \
                    .execute()
                BrokenRestriction.delete() \
                    .where(BrokenRestriction.face.in_(faces)) \
                    .execute()
                txn.commit()

                safe_delete_cluster(txn, cluster_id)

            # Send faces to warden
            with self.tracer.start_as_current_span(f'cluster-{cluster_id}-re-tag'):
                trace = get_trace_parent()

                for face_id in faces:
                    with self.tracer.start_as_current_span(face_id):
                        self.publisher_to_warden.publish(encode(MatchedFaceMessage(face_id=face_id, trace=trace)))
        else:
            with db.transaction() as txn:
                Face.delete().where(Face.id.in_(faces)).execute()
                txn.commit()

                safe_delete_cluster(txn, cluster_id)

        return jsonify(success=True)
