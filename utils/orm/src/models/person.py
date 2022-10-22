from peewee import CharField, Model

from ..database import db


class Person(Model):
    name = CharField()

    class Meta:
        database = db
        # TODO: Check how to change table name
        tablename = 'people'
