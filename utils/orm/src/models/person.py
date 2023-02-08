from peewee import CharField, DateTimeField, Model, SQL, ForeignKeyField
from playhouse.postgres_ext import ArrayField
from .person_role import PersonRole
from ..database import db


class Person(Model):
    name = CharField()
    photos = ArrayField(CharField, default=[])
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    role = ForeignKeyField(PersonRole)

    class Meta:
        database = db
        table_name = 'people'
