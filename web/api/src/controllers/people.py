from os import path
from tempfile import gettempdir

from flask import jsonify, request, send_file
from peewee import IntegrityError

from scripts.train_classifier_minio.train_classifier_minio import train_model
from utils.orm.src import Camera, Face, Person, VideoChunk, PersonPhoto
from web.api.src.controllers.known_faces import store_face_as_photo

LOCAL_DIR = gettempdir()


def _last_seen(person_id):
    face = Face.select(Face.id, Face.offset, Face.timestamp, VideoChunk.timestamp, Camera.alias) \
        .join(VideoChunk) \
        .join(Camera) \
        .where((Face.person_id == person_id) & Face.is_match) \
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
        'photos': person.photo_keys(),
        'created_at': person.created_at,
        'last_seen': _last_seen(person.id),
        'role': person.role.name
    } for person in Person.select().order_by(Person.name)]


def _update_person(person_id, name, role_id):
    if person_id == "-1":
        person_id = Person.insert(name=name, role=role_id).execute()
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


# [width * height] should measure information of a photo good enough
def _face_information_estimate(face):
    return face.bounding_box[2] * face.bounding_box[3]


class PeopleController:

    def __init__(self, people_storage, frames_storage, faces_storage):
        self.people_storage = people_storage
        self.frames_storage = frames_storage
        self.faces_storage = faces_storage

    def make_routes(self, app):
        app.route('/people')(_get_people)
        app.route('/people/<person_id>/photos/<photo>')(self._get_photo)
        app.route('/people/last_seen/<photo_id>')(self._get_last_seen_photo)
        app.route('/people/<person_id>/<name>/<role_id>', methods=["POST"])(_update_person)
        app.route('/people/<person_id>/photos', methods=["POST"])(self._add_person_photo)
        app.route('/people/<person_id>', methods=["DELETE"])(_delete_person)
        app.route('/people/add_live_photos', methods=["POST"])(self._add_live_photos)
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
            photo_key = person.next_photo_key(image.filename)

            # Upload to db
            PersonPhoto.insert(person=person.id, filename=photo_key, preprocessed=False).execute()

            # Upload photo to storage
            self.people_storage.store(photo_key, image.read())

        # Return OK
        resp = jsonify(success=True)
        return resp

    def _add_person_live_photos(self, person):
        sampling_rate_ms = 5000
        best_face = None
        initial_timestamp = 0

        for face in Face.select().where(Face.person_id == person.id).order_by(Face.timestamp.asc()):
            if best_face is None:
                best_face = face
                initial_timestamp = face.timestamp

            if face.timestamp - initial_timestamp > sampling_rate_ms:
                store_face_as_photo(person, best_face, self.faces_storage, self.people_storage)
                best_face = None
            else:
                if _face_information_estimate(face) > _face_information_estimate(best_face):
                    best_face = face

        if best_face is not None:
            store_face_as_photo(person, best_face, self.faces_storage, self.people_storage)

    def _add_live_photos(self):
        for person in Person.select():
            self._add_person_live_photos(person)

        return jsonify(success=True)

    def _train_model(self):
        train_model()

        return jsonify(success=True)
