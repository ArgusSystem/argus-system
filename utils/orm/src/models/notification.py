from peewee import BooleanField, Model, ForeignKeyField
from .user import User
from .face import Face
from .restriction import Restriction
from ..database import db


class Notification(Model):
    user = ForeignKeyField(User)
    face_id = ForeignKeyField(Face)
    restriction_id = ForeignKeyField(Restriction)
    read = BooleanField(default=False)

    class Meta:
        database = db
