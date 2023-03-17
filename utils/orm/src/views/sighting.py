from peewee import Model, BigIntegerField, IntegerField
from ..database import db


class Sighting(Model):
    camera_id = IntegerField()
    person_id = IntegerField()

    severity = IntegerField()

    start_time = BigIntegerField()
    end_time = BigIntegerField()

    class Meta:
        database = db
