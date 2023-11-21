from os import path

from .view import View
from peewee import BigIntegerField, CharField, IntegerField

SIGHTING_SQL = path.join(path.dirname(__file__), '..', '..', 'resources', 'sighting.sql')


class Sighting(View):
    camera = IntegerField()
    person = IntegerField()

    restriction = IntegerField()
    severity = CharField()

    start_time = BigIntegerField()
    end_time = BigIntegerField()

    def interval(self):
        return self.start_time, self.end_time

    def identifier(self):
        return self.camera, self.person, self.restriction

    def offender(self):
        return self.person

    @classmethod
    def create_view(cls):
        with open(SIGHTING_SQL) as file:
            query = file.read()

        return f'CREATE VIEW "sighting" AS {query}'

    @classmethod
    def drop_view(cls):
        return 'DROP VIEW IF EXISTS "sighting"'
