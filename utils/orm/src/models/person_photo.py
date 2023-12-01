from peewee import CharField, ForeignKeyField, BooleanField, Model, fn

from .person import Person
from ..database import db


class PersonPhoto(Model):
    person = ForeignKeyField(Person, null=True)
    filename = CharField()
    preprocessed = BooleanField()

    class Meta:
        database = db
