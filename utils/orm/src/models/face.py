from peewee import DecimalField, FloatField, ForeignKeyField, IntegerField, BigIntegerField, BooleanField, Model
from playhouse.postgres_ext import ArrayField

from . import VideoChunk
from .person import Person
from ..database import db


class Face(Model):
    video_chunk = ForeignKeyField(VideoChunk, backref='faces')
    offset = IntegerField()
    timestamp = BigIntegerField()
    face_num = IntegerField()

    embedding = ArrayField(FloatField)
    person = ForeignKeyField(Person, null=True)
    bounding_box = ArrayField(IntegerField, default=[])
    probability = DecimalField(decimal_places=3)
    is_match = BooleanField()

    class Meta:
        database = db

    def image_key(self):
        return '-'.join([self.frame_key(), str(self.face_num)])

    def frame_key(self):
        return '-'.join([self.video_chunk.camera.alias,
                         str(self.video_chunk.timestamp),
                         str(self.offset)])

