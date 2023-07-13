from flask import request
from peewee import fn

from utils.orm.src.models import Camera, Face, VideoChunk, UnknownCluster, UnknownFace


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
        'face_id': unknown_face.face.id,
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

    @staticmethod
    def make_routes(app):
        app.route('/unknown_clusters')(_get_unknown_clusters)
        app.route('/unknown_clusters/<cluster_id>/faces')(_get_cluster_faces)
