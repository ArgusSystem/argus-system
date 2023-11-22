from os import path

from peewee import Model
from ..database import db


class View(Model):
    class Meta:
        database = db

    @classmethod
    def create_view_str(cls):
        sql_file = path.join(path.dirname(__file__), '..', '..', 'resources', cls.view_name() + '.sql')
        with open(sql_file) as file:
            query = file.read()
        view_name_str = cls.view_name()
        return f'CREATE VIEW "{view_name_str}" AS {query}'

    @classmethod
    def drop_view_str(cls):
        view_name_str = cls.view_name()
        return f'DROP VIEW IF EXISTS "{view_name_str}"'

    @classmethod
    def view_name(cls):
        return cls.__name__.lower()
