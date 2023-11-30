from .view import View
from peewee import BigIntegerField, CharField, IntegerField


class UnknownSighting(View):
    camera = IntegerField()

    restriction = IntegerField()
    severity = CharField()

    start_time = BigIntegerField()
    end_time = BigIntegerField()

    concurrent_detections = IntegerField()

    def interval(self):
        return self.start_time, self.end_time

    def identifier(self):
        return self.camera, self.restriction

    def offender(self):
        return None
