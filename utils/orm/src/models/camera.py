from peewee import Model, CharField, DecimalField, BigIntegerField, IntegerField
from ..database import db

cameras = {}


def get_camera(camera_id):
    if camera_id not in cameras:
        cameras[camera_id] = Camera.get(Camera.alias == camera_id)

    return cameras[camera_id]


class Camera(Model):
    alias = CharField(unique=True)
    mac = BigIntegerField(unique=True)

    width = IntegerField()
    height = IntegerField()
    framerate = IntegerField()

    latitude = DecimalField(max_digits=8, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        database = db
