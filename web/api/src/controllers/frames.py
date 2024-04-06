from os import path
from tempfile import gettempdir

from flask import send_file

LOCAL_DIR = gettempdir()


class FramesController:

    def __init__(self, frames_storage):
        self.frames_storage = frames_storage

    def _get_frame_image(self, frame):
        filepath = path.join(LOCAL_DIR, frame)

        self.frames_storage.fetch(frame, filepath)

        return send_file(filepath, mimetype=f'image/jpg')

    def make_routes(self, app):
        app.route('/frames/<frame>')(self._get_frame_image)
