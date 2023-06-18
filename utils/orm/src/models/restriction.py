from peewee import BooleanField, DateTimeField, ForeignKeyField, Model, SQL
from playhouse.postgres_ext import BinaryJSONField

from . import RestrictionSeverity
from ..database import db


class Restriction(Model):
    rule = BinaryJSONField()
    last_update = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    severity = ForeignKeyField(RestrictionSeverity)
    deleted = BooleanField(default=False)

    class Meta:
        database = db
