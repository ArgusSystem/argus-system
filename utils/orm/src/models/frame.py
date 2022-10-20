from peewee import ForeignKeyField, IntegerField, Model, TimestampField

from ..database import db
from .video_chunk import VideoChunk


class Frame(Model):
    video_chunk = ForeignKeyField(VideoChunk, backref='frames')
    offset = IntegerField()
    timestamp = TimestampField()

    class Meta:
        database = db
