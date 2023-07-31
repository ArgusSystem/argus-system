from utils.orm.src.models import Face, UnknownFace
from utils.orm.src.views import Sighting
from peewee import JOIN, fn


def get_sighting_for(face_id, restriction_id):
    cte = _get_person(face_id)

    return (Sighting.select(Sighting.camera,
                            Sighting.person,
                            Sighting.matched,
                            Sighting.restriction,
                            Sighting.start_time,
                            Sighting.end_time)
            .join(cte, on=((Sighting.person == cte.c.person) & (Sighting.matched == cte.c.matched)))
            .where((Sighting.restriction == restriction_id) &
                   (Sighting.start_time <= cte.c.timestamp) &
                   (Sighting.end_time >= cte.c.timestamp))
            .with_cte(cte)
            .get())


def _get_person(face_id):
    return (Face.select(fn.COALESCE(Face.person_id, UnknownFace.cluster_id), Face.timestamp, UnknownFace.id.is_null())
            .where(Face.id == face_id)
            .join(UnknownFace, JOIN.LEFT_OUTER)
            .cte('target', columns=('person', 'timestamp', 'matched')))
