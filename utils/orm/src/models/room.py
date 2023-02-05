from peewee import CharField, Model, ForeignKeyField
from .room_type import RoomType
from ..database import db


class Room(Model):
    name = CharField()
    type = ForeignKeyField(RoomType)

    class Meta:
        database = db
