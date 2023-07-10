from peewee import fn

from utils.orm.src.models import UnknownFace


def _get_unknown_clusters():
    return [{
        'id': face.cluster_id,
        'faces_count': face.faces_count
    } for face in UnknownFace
        .select(UnknownFace.cluster_id, fn.COUNT(UnknownFace.face_id).alias('faces_count'))
        .group_by(UnknownFace.cluster_id)
        .order_by(UnknownFace.cluster_id.desc())]


class UnknownClustersController:

    @staticmethod
    def make_routes(app):
        app.route('/unknown_clusters')(_get_unknown_clusters)
