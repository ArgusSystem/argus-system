from flask import request

from utils.orm.src import Sighting


# Example: http://localhost:5000/history?person_id=0&from_date=1684810800000to_date=1684810800999
def _get_history():
    person_id = request.args.get('person_id')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    assert person_id
    assert from_date
    assert to_date

    assert from_date < to_date

    sightings = Sighting.select(Sighting.camera_id, Sighting.severity, Sighting.start_time, Sighting.end_time) \
        .where((Sighting.person_id == person_id) &
               (Sighting.start_time >= from_date) &
               (Sighting.end_time < to_date)) \
        .order_by(Sighting.start_time.desc()) \
        .execute()

    return list(map(lambda s: {'camera_id': s.camera_id,
                               'severity': s.severity,
                               'start_time': s.start_time,
                               'end_time': s.end_time},
                    sightings))


class HistoryController:

    @staticmethod
    def make_routes(app):
        app.get('/history')(_get_history)
