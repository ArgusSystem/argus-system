from os import path
from tempfile import gettempdir

from flask import send_file, jsonify

from utils.orm.src.models import Camera, VideoChunk

LOCAL_DIR = gettempdir()


def _to_json(camera):
    return {
        'id': camera.id,
        'name': camera.alias,
        'width': camera.width,
        'height': camera.height,
        'latitude': camera.latitude,
        'longitude': camera.longitude
    }


def _get_cameras():
    cameras = Camera.select(Camera.id, Camera.alias,
                            Camera.width, Camera.height,
                            Camera.latitude, Camera.longitude).execute()

    return list(map(_to_json, cameras))


def _get_camera(camera_id):
    return _to_json(Camera.get(Camera.id == camera_id))


class CameraController:

    def __init__(self, frame_storage):
        self.frame_storage = frame_storage

    def make_routes(self, app):
        app.route('/cameras')(_get_cameras)
        app.route('/cameras/<camera_id>')(_get_camera)
        app.route('/cameras/<camera_id>/frame')(self._get_frame)

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


