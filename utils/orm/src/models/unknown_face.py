from peewee import Model, ForeignKeyField
from .unknown_cluster import UnknownCluster
from .face import Face
from ..database import db


class UnknownFace(Model):
    cluster = ForeignKeyField(UnknownCluster)
    face = ForeignKeyField(Face)

    class Meta:
        database = db
