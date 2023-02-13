from random import uniform
from os import listdir, path

from utils.orm.src.database import connect
from utils.orm.src.models import Person, Camera
from utils.video_storage import StorageFactory, StorageType

#
# Setup Argus for Friends POC episode 10 season 05
#

people_storage = StorageFactory('argus', 9500, 'argus', 'panoptes').new(StorageType.PEOPLE)

connect('argus', 'argus', 5432, 'argus', 'panoptes')

# Setup people table

PEOPLE_DIR = 'people'

for i, person_name in enumerate(sorted(listdir(PEOPLE_DIR))):
    photos = []

    for photo in listdir(path.join(PEOPLE_DIR, person_name)):
        people_storage.store(name=photo, filepath=path.join(PEOPLE_DIR, person_name, photo))
        photos.append(photo)

    Person.insert(id=i, name=person_name, photos=photos).execute()


# Setup cameras table

cameras = ['joeyhouse', 'cafe', 'agent', 'street', 'rachelhouse', 'boyfriendhouse']

width = 1280
height = 720
fps = 24

cam_latitude = 40.72132
cam_longitude = -73.99773
cam_lat_long_var = -0.00155

for i, cam in enumerate(cameras):
    camera_id = Camera.insert(alias=cam,
                              mac=i,
                              width=width,
                              height=height,
                              framerate=fps,
                              latitude=cam_latitude + uniform(-cam_lat_long_var, cam_lat_long_var),
                              longitude=cam_longitude + uniform(-cam_lat_long_var, cam_lat_long_var)) \
        .execute()
