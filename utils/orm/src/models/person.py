from peewee import CharField, DateTimeField, Model, SQL, ForeignKeyField
from playhouse.postgres_ext import ArrayField
from .person_role import PersonRole
from ..database import db

people = {}


def get_person(person_id):
    if person_id not in people:
        people[person_id] = Person.get(person_id)

    return people[person_id]


class Person(Model):
    name = CharField()
    photos = ArrayField(CharField, default=[])
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    role = ForeignKeyField(PersonRole)

    class Meta:
        database = db
        table_name = 'people'
