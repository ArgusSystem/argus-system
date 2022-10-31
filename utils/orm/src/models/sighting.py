from peewee import ForeignKeyField, Model, TimestampField, CharField, BigIntegerField
from .camera import Camera
from .person import Person
from ..database import db


class Sighting(Model):
    camera = ForeignKeyField(Camera)

    person = ForeignKeyField(Person, backref='sightings')

    start_time = BigIntegerField()
    end_time = BigIntegerField()

    class Meta:
        database = db
