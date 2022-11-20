from peewee import CharField, DateTimeField, Model, SQL
from playhouse.postgres_ext import ArrayField

from ..database import db


class Person(Model):
    name = CharField()
    photos = ArrayField(CharField, default=[])
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        database = db
        table_name = 'people'
