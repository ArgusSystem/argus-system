from peewee import Model, ForeignKeyField, TimeField, IntegerField
from playhouse.postgres_ext import ArrayField
from .person_role import PersonRole
from .area_type import AreaType
from ..database import db


class Restriction(Model):
    role = ForeignKeyField(PersonRole)
    area_type = ForeignKeyField(AreaType)
    severity = IntegerField()
    time_start = TimeField()
    time_end = TimeField()

    class Meta:
        database = db
