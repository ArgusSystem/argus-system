from peewee import BooleanField, Model, ForeignKeyField
from .broken_restriction import BrokenRestriction
from .user import User
from ..database import db


class Notification(Model):
    user = ForeignKeyField(User)
    broken_restriction = ForeignKeyField(BrokenRestriction)
    read = BooleanField(default=False)

    class Meta:
        database = db
