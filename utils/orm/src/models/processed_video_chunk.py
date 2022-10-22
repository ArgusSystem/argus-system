from peewee import ForeignKeyField, Model, TimestampField

from . import VideoChunk
from ..database import db


class ProcessedVideoChunk(Model):
    video_chunk = ForeignKeyField(VideoChunk)
    # TODO: Add default to time of creation
    finished_at = TimestampField()

    class Meta:
        database = db
