from peewee import DecimalField, ForeignKeyField, IntegerField, Model
from playhouse.postgres_ext import ArrayField

from . import VideoChunk
from .person import Person
from ..database import db


class Face(Model):
    video_chunk = ForeignKeyField(VideoChunk, backref='faces')
    offset = IntegerField()

    person = ForeignKeyField(Person, null=True)
    bounding_box = ArrayField(IntegerField, default=[])
    probability = DecimalField(decimal_places=3)

    class Meta:
        database = db
