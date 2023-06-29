from os import path
from tempfile import gettempdir

from flask import send_file

LOCAL_DIR = gettempdir()


class FacesController:

    def __init__(self, faces_storage):
        self.faces_storage = faces_storage

    def _get_face(self, face):
        filepath = path.join(LOCAL_DIR, face)
        mime = "jpg"

        self.faces_storage.fetch(face, filepath)

        return send_file(filepath, mimetype=f'image/{mime}')

    def make_routes(self, app):
        app.route('/faces/<face>')(self._get_face)
