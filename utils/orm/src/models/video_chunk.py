from peewee import ForeignKeyField, IntegerField, Model, TimestampField, DecimalField
from playhouse.postgres_ext import ArrayField
from .camera import Camera
from ..database import db


class VideoChunk(Model):
    camera = ForeignKeyField(Camera)
    timestamp = TimestampField()

    duration = DecimalField(decimal_places=3)
    samples = ArrayField(IntegerField, default=[])

    class Meta:
        database = db
