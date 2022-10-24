from peewee import CharField, IntegerField, Model

from ..database import db


class Person(Model):
    name = CharField()
    dni = IntegerField()

    class Meta:
        database = db
        table_name = 'people'
