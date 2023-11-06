from peewee import BooleanField, Model
from ..database import db


class UnknownCluster(Model):

    outliers = BooleanField(default=False)

    class Meta:
        database = db
