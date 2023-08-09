from collections import defaultdict

from flask import request

from utils.orm.src.views import Sighting
from utils.time.src.timestamp import ARGENTINA_TZ, from_timestamp_ms

EPOCH_MAX_TIMESTAMP_MS = ((1 << 31) - 1) * 1000


def _to_weekday(timestamp):
    tt = from_timestamp_ms(timestamp, ARGENTINA_TZ).timetuple()
    return tt.tm_wday


def _get_sightings(start_time, end_time):
    return (Sighting
            .select(Sighting.camera, Sighting.start_time, Sighting.end_time)
            .where((Sighting.start_time >= start_time) & (Sighting.end_time <= end_time)))


def _get_visits():
    start_time = request.args.get('start', 0)
    end_time = request.args.get('end', EPOCH_MAX_TIMESTAMP_MS)

    visits = defaultdict(int)

    for s in _get_sightings(start_time, end_time):
        visits[s.camera] += 1

    return visits


def _get_week_histogram(camera):
    start_time = request.args.get('start', 0)
    end_time = request.args.get('end', EPOCH_MAX_TIMESTAMP_MS)

    histogram = [0] * 7

    for s in _get_sightings(start_time, end_time).where(Sighting.camera == camera):
        start_day = _to_weekday(s.start_time)
        end_day = _to_weekday(s.end_time)

        histogram[start_day] += 1

        if start_day != end_day:
            histogram[end_day] += 1

    total_visits = sum(histogram)

    return ['%.2f' % (h / total_visits) for h in histogram] if total_visits > 0 else histogram


def _get_avg_time_spent(camera):
    start_time = request.args.get('start', 0)
    end_time = request.args.get('end', EPOCH_MAX_TIMESTAMP_MS)

    total_time_spent = 0
    visits_count = 0

    for s in _get_sightings(start_time, end_time).where(Sighting.camera == camera):
        total_time_spent += s.end_time - s.start_time
        visits_count += 1

    return '%.2f' % (total_time_spent / visits_count) if visits_count > 0 else '0.00'


class StatisticsController:

    @staticmethod
    def make_routes(app):
        app.route('/statistics/place/visits')(_get_visits)
        app.route('/statistics/place/<camera>/week_histogram')(_get_week_histogram)
        app.route('/statistics/place/<camera>/avg_time_spent')(_get_avg_time_spent)
