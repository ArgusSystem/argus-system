from peewee import Model, ForeignKeyField
from .face import Face
from .restriction import Restriction
from ..database import db


class BrokenRestriction(Model):
    face = ForeignKeyField(Face)
    restriction = ForeignKeyField(Restriction)

    class Meta:
        database = db
