from .view import View
from peewee import BigIntegerField, CharField, IntegerField


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
