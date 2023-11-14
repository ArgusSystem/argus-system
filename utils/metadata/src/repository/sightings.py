from utils.orm.src.models import Face, UnknownFace
from utils.orm.src.views import Sighting
from peewee import Case


def get_sighting_for(face_id, restriction_id):
    cte = _get_person(face_id)

    return (Sighting.select(Sighting.camera,
                            Sighting.person,
                            Sighting.matched,
                            Sighting.restriction,
                            Sighting.start_time,
                            Sighting.end_time)
            .join(cte, on=((Sighting.person == cte.c.person) & (Sighting.matched == cte.c.is_match)))
            .where((Sighting.restriction == restriction_id) &
                   (Sighting.start_time <= cte.c.timestamp) &
                   (Sighting.end_time >= cte.c.timestamp))
            .with_cte(cte)
            .get())


def _get_person(face_id):
    return (Face.select(Case(None, [(Face.is_match, Face.person_id)], -1).alias('person'),
                        Face.timestamp, Face.is_match)
            .where(Face.id == face_id)
            .cte('target', columns=('person', 'timestamp', 'is_match')))
