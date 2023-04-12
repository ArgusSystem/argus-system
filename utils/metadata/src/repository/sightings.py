from utils.orm.src.models import Face
from utils.orm.src.views import Sighting


def get_sighting_for(face_id, restriction_id):
    return Sighting.select(Sighting.camera_id,
                           Sighting.person_id,
                           Sighting.restriction_id,
                           Sighting.start_time,
                           Sighting.end_time) \
        .join(Face, on=(Sighting.person_id == Face.person_id)) \
        .where((Face.id == face_id) &
               (Sighting.restriction_id == restriction_id) &
               (Sighting.start_time <= Face.timestamp) &
               (Sighting.end_time >= Face.timestamp)) \
        .get()
