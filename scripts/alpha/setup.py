from os import listdir, path
from random import uniform

from scripts.train_classifier_minio.train_classifier_minio import train_model
from utils.orm.src.models import (Area, AreaType, Camera, Person, PersonRole, PersonPhoto,
                                  Restriction, RestrictionSeverity, RestrictionWarden, UserPerson)
from utils.orm.src.models.user import create as create_user
from utils.orm.src.database import connect
from utils.video_storage import StorageFactory, StorageType

connect('argus', 'argus', 5432, 'argus', 'panoptes')

# Create user

user_id = create_user('argus', 'panoptes', 'gabriel')

# Setup roles

host_role_id = PersonRole.insert(name='host').execute()
guest_role_id = PersonRole.insert(name='guest').execute()
trespasser_role_id = PersonRole.insert(name='trespasser').execute()

# Setup edu and gabo

people_storage = StorageFactory('argus', 9500, 'argus', 'panoptes').new(StorageType.PEOPLE)

FACES_DIR = 'faces'


def create_person(wanted_id, person_name, role_id):

    person_id = Person.insert(id=wanted_id, name=person_name, role=role_id).execute()
    person = Person.get(id=person_id)

    for photo in listdir(path.join(FACES_DIR, person_name)):
        photo_key = person.next_photo_key(photo)
        PersonPhoto.insert(person=person_id, filename=photo_key, preprocessed=False).execute()
        people_storage.store(name=photo_key, filepath=path.join(FACES_DIR, person_name, photo))

    return person


gabo_id = create_person(0, 'gabo', host_role_id)
edu_id = create_person(1, 'edu', guest_role_id)
# lauti_id = create_person(2, 'lauti', guest_role_id)

UserPerson.insert(user_id=user_id, person_id=gabo_id).execute()

# Setup area types

public_area_type_id = AreaType.insert(name='public').execute()
private_area_type_id = AreaType.insert(name='private').execute()

# Setup 4 areas

areas = ['kitchen', 'hallway', 'study', 'bedroom']
area_types = [public_area_type_id, public_area_type_id, private_area_type_id, public_area_type_id]

area_ids = [Area.insert(name=area, type=area_type).execute() for area, area_type in zip(areas, area_types)]

# Setup cameras per area

width = 1280
height = 720
fps = 30

cam_coords = [
    [-34.61759710915304, -58.3682885202042],    # kitchen
    [-34.61793573388762, -58.36794722208188],   # hallway
    [-34.61756692160962, -58.36772394293642],   # study
    [-34.61730835828806, -58.36774148629787]    # bedroom
]

for i, area in enumerate(area_ids):
    Camera.insert(alias=areas[i],
                  area_id=area,
                  mac=i,
                  width=width,
                  height=height,
                  framerate=fps,
                  encoding='mp4',
                  latitude=cam_coords[i][0],
                  longitude=cam_coords[i][1]
                  ).execute()


def time_to_seconds(time):
    hours, minutes = time.split(':')
    return int(hours) * 3600 + int(minutes) * 60


def create_rule(type_who, value_who, rule_areas, start_time, end_time, severity):
    restriction_id = Restriction.insert(
        rule={
            'who': [
                {
                    'type': type_who,
                    'value': value_who
                }
            ],
            'where': [
                {
                    'type': 'area_type',
                    'value': rule_areas
                }
            ],
            'when': [
                {
                    'type': 'repeated',
                    'value': {
                        'start_time': time_to_seconds(start_time),
                        'end_time': time_to_seconds(end_time),
                        'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                        'time_zone': 'America/Buenos_Aires'
                    }
                }
            ]
        }, severity=severity
    ).execute()

    RestrictionWarden.insert(restriction_id=restriction_id, role_id=host_role_id).execute()


info_severity = RestrictionSeverity.insert(name='info', value=0).execute()
warning_severity = RestrictionSeverity.insert(name='warning', value=1).execute()
critical_severity = RestrictionSeverity.insert(name='critical', value=2).execute()

create_rule('role', [guest_role_id], [private_area_type_id], '00:00', '23:59', warning_severity)
create_rule('unknown', None, [public_area_type_id], '00:00', '23:59', warning_severity)
create_rule('unknown', None, [private_area_type_id], '00:00', '23:59', critical_severity)
create_rule('role', [trespasser_role_id], [public_area_type_id, private_area_type_id], '00:00', '23:59', critical_severity)

print("Training classifier model...")
train_model()
print("Training done!")
