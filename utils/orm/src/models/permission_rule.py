from peewee import Model, ForeignKeyField, TimeField
from playhouse.postgres_ext import ArrayField
from .person_role import PersonRole
from .room_type import RoomType
from ..database import db


class PermissionRule(Model):
    role = ForeignKeyField(PersonRole)
    room_type = ForeignKeyField(RoomType)
    time_start = ArrayField(TimeField)
    time_end = ArrayField(TimeField)

    class Meta:
        database = db
        table_name = 'people'
