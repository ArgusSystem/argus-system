from peewee import Model, ForeignKeyField, TimeField, IntegerField
from .person_role import PersonRole
from .area_type import AreaType
from ..database import db


class Restriction(Model):
    role = ForeignKeyField(PersonRole)
    area_type = ForeignKeyField(AreaType)
    #  0 -> Info
    #  1 -> Warning
    #  2 -> Danger
    severity = IntegerField()
    time_start = TimeField()
    time_end = TimeField()

    class Meta:
        database = db
