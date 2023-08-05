from collections import defaultdict

from utils.orm.src.views import Sighting


def _get_visits():
    visits = defaultdict(int)

    for s in Sighting.select(Sighting.camera):
        visits[s.camera] += 1

    return visits


class StatisticsController:

    @staticmethod
    def make_routes(app):
        app.route('/statistics/place/visits')(_get_visits)
