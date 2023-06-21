from peewee import CharField, IntegerField, Model
from ..database import db


class RestrictionSeverity(Model):
    name = CharField(unique=True)
    value = IntegerField()

    class Meta:
        database = db
