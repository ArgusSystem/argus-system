from peewee import Model, ForeignKeyField
from .face import Face
from .restriction import Restriction
from ..database import db


class BrokenRestriction(Model):
    face = ForeignKeyField(Face, on_delete='CASCADE', on_update='CASCADE')
    restriction = ForeignKeyField(Restriction)

    class Meta:
        database = db
