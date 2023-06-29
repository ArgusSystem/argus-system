from os import path
from tempfile import gettempdir

from flask import jsonify, request, send_file
from peewee import IntegrityError

from scripts.train_classifier_minio.train_classifier_minio import train_model
from utils.orm.src import Camera, Face, Person, VideoChunk

LOCAL_DIR = gettempdir()


def _last_seen(person_id):
    face = Face.select(Face.id, Face.offset, Face.timestamp, VideoChunk.timestamp, Camera.alias) \
        .join(VideoChunk) \
        .join(Camera) \
        .where(Face.person_id == person_id) \
        .order_by(Face.timestamp.desc()) \
        .first()

    if face:
        return {
            'place': face.video_chunk.camera.alias,
            'time': face.timestamp,
            'url': f'{face.video_chunk.camera.alias}-{face.video_chunk.timestamp}-{face.offset}'
        }

    return None


def _get_people():
    return [{
        'id': person.id,
        'name': person.name,
        'photos': person.photos,
        'created_at': person.created_at,
        'last_seen': _last_seen(person.id),
        'role': person.role.name
    } for person in Person.select().order_by(Person.name)]


def _update_person(person_id, name, role_id):
    if person_id == "-1":
        person_id = Person.insert(name=name, role=role_id, photos=[]).execute()
    else:
        Person.update(name=name, role=role_id).where(Person.id == person_id).execute()
    # Return OK
    resp = jsonify(person_id=person_id)
    return resp


def _delete_person(person_id):
    try:
        Person.delete().where(Person.id == person_id).execute()
        # Person deleted ok
        return jsonify(success=True)
    except IntegrityError:
        Person._meta.database.rollback()
        # Person is still referenced in other tables
        return jsonify(success=False), 400


class PeopleController:

    def __init__(self, people_storage, frames_storage):
        self.people_storage = people_storage
        self.frames_storage = frames_storage

    def make_routes(self, app):
        app.route('/people')(_get_people)
        app.route('/people/<person_id>/photos/<photo>')(self._get_photo)
        app.route('/people/last_seen/<photo_id>')(self._get_last_seen_photo)
        app.route('/people/<person_id>/<name>/<role_id>', methods=["POST"])(_update_person)
        app.route('/people/<person_id>/photos', methods=["POST"])(self._add_person_photo)
        app.route('/people/<person_id>', methods=["DELETE"])(_delete_person)
        app.route('/people/train', methods=["POST"])(self._train_model)

    def _get_photo(self, person_id, photo):
        filepath = path.join(LOCAL_DIR, photo)
        mime = photo.split('.')[-1]

        self.people_storage.fetch(photo, filepath)

        return send_file(filepath, mimetype=f'image/{mime}')

    def _get_last_seen_photo(self, photo_id):
        filepath = path.join(LOCAL_DIR, photo_id)
        self.frames_storage.fetch(photo_id, filepath)

        return send_file(filepath, mimetype=f'image/jpg')

    def _add_person_photo(self, person_id):
        # If person id is -1, create new person
        # if person_id == "-1":
        #     person_id = Person.insert(name=request.form.get("name"), role=request.form.get("role"), photos=[]).execute()
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
