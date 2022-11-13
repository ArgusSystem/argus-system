from peewee import CharField, Model
from playhouse.postgres_ext import ArrayField

from ..database import db


class Person(Model):
    name = CharField()
    photos = ArrayField(CharField, default=[])

    class Meta:
        database = db
        table_name = 'people'
