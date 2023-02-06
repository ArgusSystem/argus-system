from peewee import CharField, Model, ForeignKeyField
from .room_type import AreaType
from ..database import db


class Area(Model):
    name = CharField()
    type = ForeignKeyField(AreaType)

    class Meta:
        database = db
