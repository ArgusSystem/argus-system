from peewee import Model, ForeignKeyField
from .face import Face
from .restriction import Restriction
from ..database import db


class BrokenRestriction(Model):
    face_id = ForeignKeyField(Face)
    restriction_id = ForeignKeyField(Restriction)

    class Meta:
        database = db
