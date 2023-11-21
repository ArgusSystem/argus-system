from os import path

from .view import View
from peewee import BigIntegerField, CharField, IntegerField

QUERY_SQL = path.join(path.dirname(__file__), '..', '..', 'resources', 'unknown.sql')


# TODO: Group max concurrent unknown people
class UnknownSighting(View):
    camera = IntegerField()

    restriction = IntegerField()
    severity = CharField()

    start_time = BigIntegerField()
    end_time = BigIntegerField()

    def interval(self):
        return self.start_time, self.end_time

    def identifier(self):
        return self.camera, self.restriction

    def offender(self):
        return None

    @classmethod
    def create_view(cls):
        with open(QUERY_SQL) as file:
            query = file.read()

        return f'CREATE VIEW "unknownsighting" AS {query}'

    @classmethod
    def drop_view(cls):
        return 'DROP VIEW IF EXISTS "unknownsighting"'
