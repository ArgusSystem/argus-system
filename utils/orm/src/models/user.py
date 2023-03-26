from peewee import CharField, BlobField, Model
from hashlib import sha3_256

from ..database import db


class User(Model):
    username = CharField(unique=True)
    password = BlobField()

    alias = CharField()

    class Meta:
        database = db

    def is_authorized(self, password):
        return _encode(password) == self.password.tobytes()


def create(username, password, alias):
    return User(username=username, password=_encode(password), alias=alias).save()


def _encode(string):
    return sha3_256(bytes(string, 'utf-8')).digest()
