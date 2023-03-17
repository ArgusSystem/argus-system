from .view import View
from peewee import BigIntegerField, IntegerField, TextField, TimestampField


class SightingReadable(View):
    cam_alias = TextField()
    person_name = TextField()

    severity = IntegerField()

    start_time = TimestampField()
    end_time = TimestampField()

    @classmethod
    def create_view(cls):
        return 'CREATE VIEW "sighting_readable" AS ' \
                'SELECT camera.alias as cam_alias, people.name as person_name, severity, ' \
                'timestamp \'epoch\' + start_time * interval \'1 ms\' AS start_time, ' \
                'timestamp \'epoch\' + end_time * interval \'1 ms\' AS end_time ' \
                'FROM sighting ' \
                'LEFT JOIN camera ON camera.id = camera_id ' \
                'LEFT JOIN people ON people.id = person_id;'

    @classmethod
    def drop_view(cls):
        return 'DROP VIEW IF EXISTS "sighting_readable"'
