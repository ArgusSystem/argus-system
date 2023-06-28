from peewee import Model
from ..database import db


class UnknownCluster(Model):

    class Meta:
        database = db
