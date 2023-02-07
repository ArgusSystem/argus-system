from peewee import Model, ForeignKeyField, TimeField
from playhouse.postgres_ext import ArrayField
from .person_role import PersonRole
from .area_type import AreaType
from ..database import db


class PermissionRule(Model):
    role = ForeignKeyField(PersonRole)
    area_type = ForeignKeyField(AreaType)
    time_start = ArrayField(TimeField)
    time_end = ArrayField(TimeField)

    class Meta:
        database = db
        table_name = 'people'
