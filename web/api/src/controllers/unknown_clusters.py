from flask import request
from peewee import fn

from utils.orm.src.models import UnknownFace


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


class UnknownClustersController:

    @staticmethod
    def make_routes(app):
        app.route('/unknown_clusters')(_get_unknown_clusters)
