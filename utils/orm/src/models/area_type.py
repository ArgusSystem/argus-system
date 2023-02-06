from peewee import CharField, Model

from ..database import db


class AreaType(Model):
    name = CharField()

    class Meta:
        database = db
