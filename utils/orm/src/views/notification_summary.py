from .view import View
from peewee import BigIntegerField, CharField, BooleanField, ForeignKeyField, IntegerField
from playhouse.postgres_ext import ArrayField
from ..models import User, Camera, Person, Restriction


class NotificationSummary(View):
    user = ForeignKeyField(User)

    camera = ForeignKeyField(Camera)
    person = ForeignKeyField(Person)
    is_unknown = BooleanField()

    restriction = ForeignKeyField(Restriction)
    severity = CharField()

    start_time = BigIntegerField()
    end_time = BigIntegerField()

    read = BooleanField()
    notification_ids = ArrayField(IntegerField, default=[])
