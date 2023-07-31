from .view import View
from peewee import BigIntegerField, BooleanField, CharField, IntegerField


class Sighting(View):
    camera = IntegerField()
    person = IntegerField()
    matched = BooleanField()

    restriction = IntegerField()
    severity = CharField()

    start_time = BigIntegerField()
    end_time = BigIntegerField()

    def interval(self):
        return self.start_time, self.end_time

    @classmethod
    def create_view(cls):
        return 'CREATE VIEW "sighting" AS ' \
               'SELECT camera, person, matched, severity, restriction, min(TIMESTAMP) AS start_time,  max(TIMESTAMP) AS end_time ' \
               'FROM (' \
                    'SELECT timestamp, camera, person, matched, restriction, severity, count(is_reset) OVER (ORDER BY person, matched, timestamp) AS grp ' \
                    'FROM (' \
                        'SELECT timestamp,' \
                               'camera,' \
                               'person,' \
                               'matched,' \
                               'restriction,' \
                               'severity,' \
                               'CASE WHEN lag(camera) OVER (ORDER BY person, matched, timestamp) <> camera ' \
                                             'OR lag(person) OVER (ORDER BY person, matched, timestamp) <> person ' \
                                             'OR lag(matched) OVER (ORDER BY person, matched, timestamp) <> matched ' \
                                             'OR lag(severity) OVER (ORDER BY person, matched, timestamp) <> severity ' \
                                   'THEN 1 END as is_reset ' \
                        'FROM (SELECT camera.id                                        as camera,' \
                                     'COALESCE(face.person_id, unknownface.cluster_id) as person,' \
                                     'face.is_match                                    as matched,' \
                                     'face.timestamp                                   as timestamp,' \
                                     'restriction.id                                   as restriction,' \
                                     'restrictionseverity.name                         as severity ' \
                              'FROM face ' \
                              'LEFT JOIN videochunk ON face.video_chunk_id = videochunk.id ' \
                              'LEFT JOIN camera ON videochunk.camera_id = camera.id ' \
                              'LEFT JOIN brokenrestriction ON brokenrestriction.face_id = face.id ' \
                              'LEFT JOIN restriction ON brokenrestriction.restriction_id = restriction.id ' \
                              'LEFT JOIN restrictionseverity ON restriction.severity_id = restrictionseverity.id ' \
                              'LEFT JOIN unknownface on face.id = unknownface.face_id ' \
                              'ORDER BY person, matched, timestamp' \
                              ') AS tmp' \
                        ') AS t ' \
                    ') AS G ' \
                'GROUP BY camera, person, matched, restriction, severity, grp ' \
                'ORDER BY end_time;'

    @classmethod
    def drop_view(cls):
        return 'DROP VIEW IF EXISTS "sighting"'
