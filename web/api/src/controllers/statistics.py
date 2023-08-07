from collections import defaultdict

from flask import request

from utils.orm.src.views import Sighting

EPOCH_MAX_TIMESTAMP_MS = ((1 << 31) - 1) * 1000


def _get_visits():
    start_time = request.args.get('start', 0)
    end_time = request.args.get('end', EPOCH_MAX_TIMESTAMP_MS)

    visits = defaultdict(int)

    for s in (Sighting
            .select(Sighting.camera)
            .where((Sighting.start_time >= start_time) & (Sighting.end_time <= end_time))):
        visits[s.camera] += 1

    return visits


class StatisticsController:

    @staticmethod
    def make_routes(app):
        app.route('/statistics/place/visits')(_get_visits)
