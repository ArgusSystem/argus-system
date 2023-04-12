from .view import View
from peewee import BigIntegerField, IntegerField


class Sighting(View):
    camera_id = IntegerField()
    person_id = IntegerField()

    restriction_id = IntegerField()
    severity = IntegerField()

    start_time = BigIntegerField()
    end_time = BigIntegerField()

    def interval(self):
        return self.start_time, self.end_time

    @classmethod
    def create_view(cls):
        return 'CREATE VIEW "sighting" AS ' \
               'SELECT id AS camera_id, person_id, severity, restriction_id, min(TIMESTAMP) AS start_time,  max(TIMESTAMP) AS end_time ' \
                'FROM ( ' \
                    'SELECT timestamp, id, person_id, restriction_id, severity, count(is_reset) OVER (ORDER BY person_id, timestamp) AS grp ' \
                    'FROM ( ' \
                        'SELECT timestamp, id, person_id, restriction_id, severity,' \
                        'CASE WHEN lag(id) OVER (ORDER BY person_id, timestamp) <> id ' \
                        'OR lag(person_id) OVER (ORDER BY person_id, TIMESTAMP) <> person_id ' \
                        'OR lag(severity) OVER (ORDER BY person_id, TIMESTAMP) <> severity ' \
                        'THEN 1 END AS is_reset ' \
                        'FROM ( ' \
                            'SELECT camera.id, face.person_id,  ' \
                            'face.timestamp AS TIMESTAMP, restriction.id as restriction_id, coalesce(restriction.severity, -1) AS severity ' \
                            'FROM face ' \
                            'LEFT JOIN videochunk ON video_chunk_id = videochunk.id ' \
                            'LEFT JOIN camera ON camera_id = camera.id ' \
                            'LEFT JOIN brokenrestriction ON brokenrestriction.face_id = face.id ' \
                            'LEFT JOIN restriction ON brokenrestriction.restriction_id = restriction.id ' \
                            'WHERE is_match = TRUE ' \
                            'ORDER BY person_id, TIMESTAMP) AS tmp ' \
                        ') AS t ' \
                    ') AS G ' \
                'GROUP BY id, person_id, restriction_id, severity, grp ' \
                'ORDER BY MIN(TIMESTAMP) ASC;'

    @classmethod
    def drop_view(cls):
        return 'DROP VIEW IF EXISTS "sighting"'
