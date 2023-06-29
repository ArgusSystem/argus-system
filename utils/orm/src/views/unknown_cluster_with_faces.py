from .view import View
from playhouse.postgres_ext import ArrayField
from peewee import CharField, IntegerField


class UnknownClusterWithFaces(View):
    id = IntegerField()
    faces = ArrayField(CharField, default=[])

    class Meta:
        table_name = 'unknown_cluster_with_faces'

    @classmethod
    def create_view(cls):
        return 'CREATE VIEW "unknown_cluster_with_faces" AS ' \
               'SELECT cluster_id as id, array_agg(face_minio_id) AS faces ' \
               'FROM (SELECT cluster_id, camera.alias || \'-\' || videochunk.timestamp || \'-\' || face.offset || \'-\' || face.face_num AS face_minio_id ' \
               'FROM unknownface ' \
               'LEFT JOIN face ON face_id = face.id ' \
               'LEFT JOIN videochunk ON video_chunk_id = videochunk.id ' \
               'LEFT JOIN camera ON camera_id = camera.id) AS t ' \
               'GROUP BY cluster_id ' \
               'ORDER BY cluster_id;' \

    @classmethod
    def drop_view(cls):
        return 'DROP VIEW IF EXISTS "unknown_cluster_with_faces"'
