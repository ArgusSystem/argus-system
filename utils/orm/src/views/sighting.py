from .view import View
from peewee import BigIntegerField, CharField, IntegerField


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
