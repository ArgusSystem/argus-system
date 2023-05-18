from peewee import ForeignKeyField, Model

from .person import Person
from .user import User
from ..database import db


class UserPerson(Model):
    user = ForeignKeyField(User)
    person = ForeignKeyField(Person)

    class Meta:
        database = db

        indexes = (
            (('user', 'person'), True),
        )
