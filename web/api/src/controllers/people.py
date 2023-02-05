from os import path
from tempfile import gettempdir
from zoneinfo import ZoneInfo

from flask import send_file, request, jsonify
import datetime

from utils.orm.src import Person, Face
from scripts.train_classifier_minio.train_classifier_minio import train_model

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
    face = Face.select(Face.timestamp) \
        .where(Face.person_id == person_id) \
        .order_by(Face.timestamp.desc()) \
        .first()
    if face:
        return _local_time(datetime.datetime.fromtimestamp(face.timestamp / 1e3))
    return None


def _get_people():
    people = Person.select(Person.id, Person.name, Person.photos, Person.created_at).order_by(Person.name).execute()

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
        app.route('/people/<person_id>/photos', methods=["POST"])(self._add_person_photo)
        app.route('/people/train', methods=["POST"])(self._train_model)

    def _get_photo(self, person_id, photo):
        filepath = path.join(LOCAL_DIR, photo)
        mime = photo.split('.')[-1]

        self.people_storage.fetch(photo, filepath)

        return send_file(filepath, mimetype=f'image/{mime}')

    def _add_person_photo(self, person_id):
        # If person id is -1, create new person
        if person_id == "-1":
            person_id = Person.insert(name=request.form.get("name"), photos=[]).execute()
        person = Person.get(Person.id == person_id)

        # For each photo received
        for name in request.files:
            image = request.files[name]

            # Determine new photo id
            new_photo_number = 1
            if len(person.photos) > 0:
                new_photo_number = max([int(''.join(c for c in name if c.isdigit())) for name in person.photos]) + 1
            new_photo_id = person.name + "_" + str(new_photo_number).zfill(3) + "." + image.filename.split(".")[1]
            person.photos.append(new_photo_id)

            # Upload photo to storage
            self.people_storage.store(new_photo_id, image.read())

        # Add all photos to person's list in db
        person.save()

        # Return OK
        resp = jsonify(success=True)
        return resp

    def _train_model(self):
        train_model()

        # Return OK
        resp = jsonify(success=True)
        return resp
