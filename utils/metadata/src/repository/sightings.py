from utils.orm.src.models import Face
from utils.orm.src.views import Sighting


# TODO: Need to rethink how to use restriction_id, talk to Gabo
def get_sighting_for(face_id):
    return Sighting.select(Sighting.person_id,
                           Sighting.camera_id,
                           Sighting.severity,
                           Sighting.start_time,
                           Sighting.end_time) \
        .join(Face, on=(Sighting.person_id == Face.person_id)) \
        .where((Face.id == face_id) &
               (Sighting.start_time <= Face.timestamp) &
               (Sighting.end_time >= Face.timestamp)) \
        .get()
