from random import uniform
from os import listdir, path

from utils.orm.src.database import connect
from utils.orm.src.models import PersonRole, Person, Camera, AreaType, Area, Restriction, RestrictionWarden
from utils.orm.src.models.user import create as create_user
from utils.video_storage import StorageFactory, StorageType
from scripts.train_classifier_minio.train_classifier_minio import train_model

#
# Setup Argus for Friends POC episode 10 season 05
#

people_storage = StorageFactory('argus', 9500, 'argus', 'panoptes').new(StorageType.PEOPLE)

connect('argus', 'argus', 5432, 'argus', 'panoptes')

# Create user

user_id = create_user('argus', 'panoptes', 'argus')

# Setup person roles table

friend_role_id = PersonRole.insert(name='friend').execute()
warden_role_id = PersonRole.insert(name='friend').execute()

# Setup people table

PEOPLE_DIR = 'people'

for i, person_name in enumerate(sorted(listdir(PEOPLE_DIR))):
    photos = []

    for photo in listdir(path.join(PEOPLE_DIR, person_name)):
        people_storage.store(name=photo, filepath=path.join(PEOPLE_DIR, person_name, photo))
        photos.append(photo)

    person_id = Person.insert(id=i, name=person_name, photos=photos, role=friend_role_id) \
        .on_conflict(action='IGNORE') \
        .execute()

# Setup area types table

area_types = ['public']
area_type_id = AreaType.insert(name=area_types[0]).execute()

# Steup areas table

areas = ['joeyhouse', 'cafe', 'agent', 'street', 'rachelhouse', 'boyfriendhouse']
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

restrictions_time = [
    ['10:38', '10:39'],
    ['10:51', '10:52'],
    ['10:58', '11:02']
]

for i, restriction_time in enumerate(restrictions_time):
    restriction_id = Restriction.insert(role=friend_role_id,
                                        area_type=area_type_id,
                                        severity=i,
                                        time_start=restriction_time[0],
                                        time_end=restriction_time[1]) \
        .execute()

    RestrictionWarden.insert(restriction_id=restriction_id, role_id=warden_role_id).execute()

# Train classifier model
print("Training classifier model...")
train_model()
print("Training done!")
