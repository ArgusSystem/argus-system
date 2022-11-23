from os import path
from tempfile import gettempdir
from zoneinfo import ZoneInfo

from flask import send_file

from utils.orm.src import Person, Face

LOCAL_DIR = gettempdir()

TIME_FORMAT = '%d %b %Y %H:%M:%S'
UTC = ZoneInfo('UTC')
LOCAL_TIME = ZoneInfo('America/Argentina/Buenos_Aires')


def _local_time(date):
    return date \
        .replace(tzinfo=UTC) \
        .astimezone(LOCAL_TIME) \
        .strftime(TIME_FORMAT)


def _last_seen(person_id):
    return Face.select(Face.timestamp) \
        .where(Face.person_id == person_id) \
        .order_by(Face.timestamp.desc()) \
        .get_or_none()


def _get_people():
    people = Person.select(Person.id, Person.name, Person.photos, Person.created_at).execute()

    return list(map(lambda person: {
        'id': person.id,
        'text': person.name,
        'photos': person.photos,
        'created_at': _local_time(person.created_at),
        'last_seen': _last_seen(person.id)
    }, people))


class PeopleController:

    def __init__(self, people_storage):
        self.people_storage = people_storage

    def make_routes(self, app):
        app.route('/people')(_get_people)
        app.route('/people/<person_id>/photos/<photo>')(self._get_photo)

    def _get_photo(self, person_id, photo):
        filepath = path.join(LOCAL_DIR, photo)
        mime = photo.split('.')[-1]

        self.people_storage.fetch(photo, filepath)

        return send_file(filepath, mimetype=f'image/{mime}')
