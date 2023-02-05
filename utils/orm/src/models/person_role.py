from peewee import CharField, Model

from ..database import db


class PersonRole(Model):
    name = CharField()

    class Meta:
        database = db
