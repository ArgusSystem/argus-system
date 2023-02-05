from peewee import CharField, Model

from ..database import db


class RoomType(Model):
    name = CharField()

    class Meta:
        database = db
