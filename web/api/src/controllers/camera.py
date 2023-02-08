from os import path
from tempfile import gettempdir

from flask import send_file, jsonify

from utils.orm.src.models import Camera, VideoChunk
from peewee import IntegrityError

LOCAL_DIR = gettempdir()


def _to_json(camera):
    return {
        'id': camera.id,
        'name': camera.alias,
        'mac': camera.mac,
        'width': camera.width,
        'height': camera.height,
        'latitude': camera.latitude,
        'longitude': camera.longitude,
        'area': camera.area.name
    }


def _get_cameras():
    cameras = Camera.select().execute()

    return list(map(_to_json, cameras))


def _get_camera(camera_id):
    return _to_json(Camera.get(Camera.id == camera_id))


def _update_camera(camera_id, alias, mac, area, latitude, longitude):
    if camera_id == "-1":
        camera_id = Camera.insert(alias=alias, mac=mac, area=area, latitude=latitude, longitude=longitude).execute()
    else:
        Camera.update(alias=alias, mac=mac, area=area, latitude=latitude, longitude=longitude)\
            .where(Camera.id == camera_id).execute()
    # Return OK
    resp = jsonify(camera_id=camera_id)
    return resp


def _delete_camera(camera_id):
    try:
        Camera.delete().where(Camera.id == camera_id).execute()
        # Role deleted ok
        return jsonify(success=True)
    except IntegrityError:
        Camera._meta.database.rollback()
        # Role is still referenced in other tables
        return jsonify(success=False), 400


class CameraController:

    def __init__(self, frame_storage):
        self.frame_storage = frame_storage

    def make_routes(self, app):
        app.route('/cameras')(_get_cameras)
        app.route('/cameras/<camera_id>')(_get_camera)
        app.route('/cameras/<camera_id>/frame')(self._get_frame)
        app.route('/cameras/<camera_id>/<alias>/<mac>/<area>/<latitude>/<longitude>', methods=["POST"])(_update_camera)
        app.route('/cameras/<camera_id>', methods=["DELETE"])(_delete_camera)

    def _get_frame(self, camera_id):
        filepath = path.join(LOCAL_DIR, camera_id)

        try:
            video_chunk = VideoChunk \
                .select() \
                .join(Camera) \
                .where(Camera.id == camera_id) \
                .order_by(VideoChunk.timestamp.desc()) \
                .get()
            frame = f'{video_chunk.camera.alias}-{video_chunk.timestamp}-{video_chunk.samples[-1]}'
            self.frame_storage.fetch(frame, filepath)
            return send_file(filepath, mimetype='image/jpeg')
        except:
            resp = jsonify(success=True)
            return resp


