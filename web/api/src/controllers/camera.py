from utils.orm.src.models.camera import Camera


def _get_cameras():
    cameras = Camera.select(Camera.id, Camera.alias, Camera.latitude, Camera.longitude).execute()

    return list(map(lambda camera: {'id': camera.id,
                                    'name': camera.alias,
                                    'latitude': camera.latitude,
                                    'longitude': camera.longitude},
                    cameras))


class CameraController:

    @staticmethod
    def make_routes(app):
        app.route('/camera')(_get_cameras)
