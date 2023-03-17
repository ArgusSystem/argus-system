from peewee import Model
from ..database import db


class View(Model):
    class Meta:
        database = db
