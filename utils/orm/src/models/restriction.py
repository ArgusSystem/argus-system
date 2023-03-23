from peewee import Model, ForeignKeyField, TimeField, IntegerField
from .person_role import PersonRole
from .area_type import AreaType
from ..database import db


class Restriction(Model):
    offender_role = ForeignKeyField(PersonRole)
    area_type = ForeignKeyField(AreaType)
    severity = IntegerField()
    time_start = TimeField()
    time_end = TimeField()
    warden_role = ForeignKeyField(PersonRole)

    class Meta:
        database = db
