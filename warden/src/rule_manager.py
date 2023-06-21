from threading import Event, Timer

from utils.metadata.src.rules import Rule
from utils.orm.src.models import Area, Camera, Face, Person, Restriction, VideoChunk

REFRESH_TIME = 10.0


def _fetch_rules():
    return [Rule(restriction.id, restriction.rule, restriction.last_update)
            for restriction in Restriction.select().where(~Restriction.deleted)]


def _get_face(face_id):
    return Face.select(Face, Person, VideoChunk, Camera, Area) \
        .join(Person).switch(Face).join(VideoChunk).join(Camera).join(Area) \
        .where(Face.id == face_id) \
        .get()


def _create_timer(callback):
    return Timer(REFRESH_TIME, callback)


class RuleManager:

    def __init__(self):
        self.rules = _fetch_rules()
        self.refresh_event = Event()
        self._start_refresh_timer()

    def _start_refresh_timer(self):
        Timer(REFRESH_TIME, lambda: self.refresh_event.set()).start()

    def execute(self, face_id):
        if self.refresh_event.is_set():
            self.rules = _fetch_rules()
            self.refresh_event.clear()
            self._start_refresh_timer()

        face = _get_face(face_id)

        return map(lambda rule: rule.id,
                   filter(lambda rule: rule.match(person=face.person.id,
                                                  role=face.person.role_id,
                                                  camera=face.video_chunk.camera.id,
                                                  area=face.video_chunk.camera.area.id,
                                                  area_type=face.video_chunk.camera.area.type_id,
                                                  timestamp=face.timestamp),
                          self.rules))
