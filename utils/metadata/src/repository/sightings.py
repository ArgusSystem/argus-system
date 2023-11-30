from utils.orm.src.models import Face
from utils.orm.src.views import Sighting, UnknownSighting

UNKNOWN = (UnknownSighting, [UnknownSighting.camera, UnknownSighting.restriction, UnknownSighting.start_time,
                             UnknownSighting.end_time])


def get_sighting_for(face_id, restriction_id):
    face = _get_face(face_id)

    return _fetch_sighting(face, restriction_id) if face.is_match else _fetch_unknown_sighting(face, restriction_id)


def _fetch_sighting(face, restriction_id):
    return (Sighting
            .select(Sighting.camera,
                    Sighting.person,
                    Sighting.restriction,
                    Sighting.start_time,
                    Sighting.end_time)
            .where((Sighting.restriction == restriction_id) &
                   (Sighting.person == face.person_id) &
                   (Sighting.start_time <= face.timestamp) &
                   (Sighting.end_time >= face.timestamp))
            .get())


def _fetch_unknown_sighting(face, restriction_id):
    return (UnknownSighting
            .select(UnknownSighting.camera,
                    UnknownSighting.restriction,
                    UnknownSighting.start_time,
                    UnknownSighting.end_time)
            .where((UnknownSighting.restriction == restriction_id) &
                   (UnknownSighting.start_time <= face.timestamp) &
                   (UnknownSighting.end_time >= face.timestamp))
            .get())


def _get_face(face_id):
    return (Face.select(Face.person_id, Face.is_match, Face.timestamp)
            .where(Face.id == face_id)
            .get())
