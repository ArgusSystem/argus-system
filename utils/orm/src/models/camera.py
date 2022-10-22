from peewee import Model, CharField, DecimalField, BigIntegerField, IntegerField
from ..database import db


class Camera(Model):
    alias = CharField(unique=True)
    mac = BigIntegerField(unique=True)

    width = IntegerField()
    height = IntegerField()
    framerate = IntegerField()

    latitude = DecimalField(max_digits=8, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        database = db
