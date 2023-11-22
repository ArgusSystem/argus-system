from peewee import Model, ForeignKeyField
from .unknown_cluster import UnknownCluster
from .face import Face
from ..database import db


class UnknownFace(Model):
    cluster = ForeignKeyField(UnknownCluster)
    face = ForeignKeyField(Face, on_delete='CASCADE', on_update='CASCADE')

    class Meta:
        database = db
