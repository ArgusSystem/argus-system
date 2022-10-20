from peewee import ForeignKeyField, Model, TimestampField, DecimalField
from .camera import Camera
from ..database import db


class VideoChunk(Model):
    camera = ForeignKeyField(Camera)
    timestamp = TimestampField()

    duration = DecimalField(decimal_places=3)

    class Meta:
        database = db
