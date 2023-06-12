from peewee import DateTimeField, IntegerField, Model, SQL
from playhouse.postgres_ext import BinaryJSONField

from ..database import db


class Restriction(Model):
    rule = BinaryJSONField()
    last_update = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    #  0 -> Info
    #  1 -> Warning
    #  2 -> Danger
    severity = IntegerField()

    class Meta:
        database = db
