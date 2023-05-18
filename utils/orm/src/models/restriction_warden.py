from peewee import ForeignKeyField, Model

from . import Restriction, PersonRole
from ..database import db


class RestrictionWarden(Model):
    restriction = ForeignKeyField(Restriction)
    role = ForeignKeyField(PersonRole)

    class Meta:
        database = db

        indexes = (
            (('restriction', 'role'), True),
        )
