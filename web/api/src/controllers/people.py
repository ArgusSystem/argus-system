from os import path
from tempfile import gettempdir

from flask import send_file

from utils.orm.src import Person

LOCAL_DIR = gettempdir()


def _get_people():
    people = Person.select(Person.id, Person.name, Person.photos).execute()
    return list(map(lambda person: {
        'id': person.id,
        'text': person.name,
        'photos': person.photos
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
