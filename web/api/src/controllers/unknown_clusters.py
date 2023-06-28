from flask import jsonify

from utils.orm.src import UnknownClusterWithFaces


def _get_unknown_clusters():
    unknown_clusters = UnknownClusterWithFaces.select().execute()
    result = list(map(lambda cluster: {
        'id': cluster.id,
        'faces': cluster.faces
    }, unknown_clusters))
    print(result)
    return result


class UnknownClustersController:

    @staticmethod
    def make_routes(app):
        app.route('/unknownclusters')(_get_unknown_clusters)
