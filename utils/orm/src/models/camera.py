from peewee import Model, CharField, DecimalField, BigIntegerField, IntegerField, ForeignKeyField
from ..database import db
from .area import Area

cameras = {}


def get_camera(camera_id):
    if camera_id not in cameras:
        cameras[camera_id] = Camera.get(Camera.alias == camera_id)

    return cameras[camera_id]


class Camera(Model):
    alias = CharField(unique=True)
    mac = BigIntegerField(unique=True)

    width = IntegerField(default=640)
    height = IntegerField(default=480)
    framerate = IntegerField(default=30)

    encoding = CharField()

    latitude = DecimalField(max_digits=16, decimal_places=14)
    longitude = DecimalField(max_digits=16, decimal_places=14)

    area = ForeignKeyField(Area)

    class Meta:
        database = db
