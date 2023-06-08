from peewee import Model, ForeignKeyField, TimeField, IntegerField
from playhouse.postgres_ext import BinaryJSONField
from .person_role import PersonRole
from .area_type import AreaType
from ..database import db


class Restriction(Model):
    rule = BinaryJSONField()
    #  0 -> Info
    #  1 -> Warning
    #  2 -> Danger
    severity = IntegerField()

    role = ForeignKeyField(PersonRole)
    area_type = ForeignKeyField(AreaType)
    time_start = TimeField()
    time_end = TimeField()

    class Meta:
        database = db
