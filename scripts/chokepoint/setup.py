from random import uniform
from os import listdir, path

import pytz

from utils.orm.src.database import connect
from utils.orm.src.models import PersonRole, Person, Camera, AreaType, Area, Restriction, RestrictionSeverity, \
    RestrictionWarden, UserPerson
from utils.orm.src.models.user import create as create_user
from utils.video_storage import StorageFactory, StorageType
from scripts.train_classifier_minio.train_classifier_minio import train_model


people_storage = StorageFactory('argus', 9500, 'argus', 'panoptes').new(StorageType.PEOPLE)

connect('argus', 'argus', 5432, 'argus', 'panoptes')

# Create user

user_id = create_user('argus', 'panoptes', 'argus')

# Setup person roles table

friend_role_id = PersonRole.insert(name='friend').execute()
warden_role_id = PersonRole.insert(name='warden').execute()

# Setup people table

PEOPLE_DIR = 'people'
person_id = 0

for person_name in sorted(listdir(PEOPLE_DIR)):
    photos = []

    for photo in listdir(path.join(PEOPLE_DIR, person_name)):
        people_storage.store(name=photo, filepath=path.join(PEOPLE_DIR, person_name, photo))
        photos.append(photo)

    Person.insert(id=person_id, name=person_name, photos=photos, role=friend_role_id).execute()

    person_id += 1

Person.insert(id=person_id, name='warden', role=warden_role_id).execute()
UserPerson.insert(user_id=user_id, person_id=person_id).execute()

# Setup area types table

area_types = ['public']
area_type_id = AreaType.insert(name=area_types[0]).execute()

# Steup areas table

areas = ['hallway_1']
areas_ids = []
for area in areas:
    area_id = Area.insert(name=area, type=area_type_id).execute()
    areas_ids.append(area_id)

# Setup cameras table

width = 1280
height = 720
fps = 24

cam_latitude = 40.72132
cam_longitude = -73.99773
cam_lat_long_var = -0.00155

for i, area in enumerate(areas_ids):
    camera_id = Camera.insert(alias=areas[i],
                              area_id=area,
                              mac=i,
                              width=width,
                              height=height,
                              framerate=fps,
                              latitude=cam_latitude + uniform(-cam_lat_long_var, cam_lat_long_var),
                              longitude=cam_longitude + uniform(-cam_lat_long_var, cam_lat_long_var)) \
        .execute()

# Setup restrictions table


severities = [
    RestrictionSeverity.insert(name=name, value=i).execute() for i, name in enumerate(['info', 'warning', 'danger'])
]

restrictions_time = [
    ['7:38', '7:39'],
    ['7:51', '7:52'],
    ['7:58', '8:02']
]


def time_to_seconds(time):
    hours, minutes = time.split(':')
    return int(hours) * 3600 + int(minutes) * 60


for i, restriction_time in enumerate(restrictions_time):
    restriction_id = Restriction.insert(
        rule={
            'who': [
                {
                    'type': 'role',
                    'value': [friend_role_id]
                }
            ],
            'where': [
                {
                    'type': 'area_type',
                    'value': [area_type_id]
                }
            ],
            'when': [
                {
                    'type': 'repeated',
                    'value': {
                        'start_time': time_to_seconds(restriction_time[0]),
                        'end_time': time_to_seconds(restriction_time[1]),
                        'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                        'time_zone': 'America/Buenos_Aires'
                    }
                }
            ]
        },
        # Only 3 possible severities
        severity=severities[i % len(severities)]) \
        .execute()

    RestrictionWarden.insert(restriction_id=restriction_id, role_id=warden_role_id).execute()

# Train classifier model
print("Training classifier model...")
train_model()
print("Training done!")
