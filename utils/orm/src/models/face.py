from peewee import DecimalField, ForeignKeyField, IntegerField, BigIntegerField, BooleanField, Model
from playhouse.postgres_ext import ArrayField

from . import VideoChunk
from .person import Person
from ..database import db


class Face(Model):
    video_chunk = ForeignKeyField(VideoChunk, backref='faces')
    offset = IntegerField()
    timestamp = BigIntegerField()
    face_num = IntegerField()

    person = ForeignKeyField(Person, null=True)
    bounding_box = ArrayField(IntegerField, default=[])
    probability = DecimalField(decimal_places=3)
    is_match = BooleanField()

    class Meta:
        database = db
