from os import listdir, path
from random import uniform

from scripts.train_classifier_minio.train_classifier_minio import train_model
from utils.orm.src import Area, AreaType, Camera, Person, PersonRole, UserPerson
from utils.orm.src.database import connect

from utils.orm.src.models.user import create as create_user
from utils.video_storage import StorageFactory, StorageType

# Connect to database

connect('argus', 'argus', 5432, 'argus', 'panoptes')


# Create user

user_id = create_user('argus', 'panoptes', 'argus')


# Create roles and people

dweller_role_id = PersonRole.insert(name='dweller').execute()
warden_role_id = PersonRole.insert(name='warden').execute()

people_storage = StorageFactory('argus', 9500, 'argus', 'panoptes').new(StorageType.PEOPLE)

PEOPLE_DIR = '../datasets/scene_of_the_crime/people'
person_id = 0

for person_name in sorted(listdir(PEOPLE_DIR)):
    photos = []

    for photo in listdir(path.join(PEOPLE_DIR, person_name)):
        people_storage.store(name=photo, filepath=path.join(PEOPLE_DIR, person_name, photo))
        photos.append(photo)

    Person.insert(id=person_id, name=person_name, photos=photos, role=dweller_role_id).execute()

    person_id += 1

Person.insert(id=person_id, name='warden', role=warden_role_id).execute()
UserPerson.insert(user_id=user_id, person_id=person_id).execute()


# Setup area types

area_type_id = AreaType.insert(name='house').execute()

# Setup areas

areas = ['bathroom', 'bedroom', 'deck', 'hall', 'kitchen', 'living_room', 'study']
areas_ids = [Area.insert(name=area, type=area_type_id).execute() for area in areas]


# Setup cameras table

width = 1280
height = 720
fps = 30

cam_latitude = 40.72132
cam_longitude = -73.99773
cam_lat_long_var = 0.00155

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


print("Training classifier model...")
train_model(True)
print("Training done!")
