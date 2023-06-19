from utils.metadata.src.rules import Rule
from utils.orm.src.models import Area, Camera, Face, Person, Restriction, VideoChunk


def _fetch_rules():
    return [Rule(restriction.id, restriction.rule, restriction.last_update)
            for restriction in Restriction.select().where(~Restriction.deleted)]


def _get_face(face_id):
    return Face.select(Face, Person, VideoChunk, Camera, Area) \
        .join(Person).switch(Face).join(VideoChunk).join(Camera).join(Area) \
        .where(Face.id == face_id) \
        .get()


class RuleManager:

    def __init__(self):
        self.rules = _fetch_rules()

    def execute(self, face_id):
        face = _get_face(face_id)

        return map(lambda rule: rule.id,
                   filter(lambda rule: rule.match(person=face.person.id,
                                                  role=face.person.role_id,
                                                  camera=face.video_chunk.camera.id,
                                                  area=face.video_chunk.camera.area.id,
                                                  area_type=face.video_chunk.camera.area.type_id,
                                                  timestamp=face.timestamp),
                          self.rules))
