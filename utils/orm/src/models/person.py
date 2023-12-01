from peewee import CharField, DateTimeField, Model, SQL, ForeignKeyField, fn
from playhouse.postgres_ext import ArrayField
from .person_role import PersonRole
from ..database import db

people = {}


def get_person(person_id):
    if person_id not in people:
        people[person_id] = Person.get(person_id)

    return people[person_id]


class Person(Model):
    name = CharField()
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    role = ForeignKeyField(PersonRole)

    class Meta:
        database = db
        table_name = 'people'

    def photo_keys(self):
        return [person_photo.filename for person_photo in self.photos()]

    def photos(self):
        from .person_photo import PersonPhoto
        return PersonPhoto.select().where(PersonPhoto.person == self.id)

    def next_photo_key(self, orig_photo_filename="aa.jpg"):
        ext = orig_photo_filename.split(".")[1]
        sep = "_"
        my_photos = self.photo_keys()
        new_photo_number = 1
        if len(my_photos) > 0:
            new_photo_number = max([int(name.split(sep)[1].split(".")[0]) for name in my_photos]) + 1
        return self.name + sep + str(new_photo_number).zfill(3) + "." + ext
