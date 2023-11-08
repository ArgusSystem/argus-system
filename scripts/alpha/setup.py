from os import listdir, path
from random import uniform

from scripts.train_classifier_minio.train_classifier_minio import train_model
from utils.orm.src.models import Area, AreaType, Camera, Person, PersonRole, UserPerson
from utils.orm.src.models.user import create as create_user
from utils.orm.src.database import connect
from utils.video_storage import StorageFactory, StorageType

connect('argus', 'argus', 5432, 'argus', 'panoptes')

# Create user

user_id = create_user('argus', 'panoptes', 'gabriel')

# Setup roles

dweller_role_id = PersonRole.insert(name='host').execute()
guest_role_id = PersonRole.insert(name='guest').execute()

# Setup edu and gabo

people_storage = StorageFactory('argus', 9500, 'argus', 'panoptes').new(StorageType.PEOPLE)

FACES_DIR = 'faces'


def create_person(person_id, person_name, role_id):
    photos = []

    for photo in listdir(path.join(FACES_DIR, person_name)):
        people_storage.store(name=photo, filepath=path.join(FACES_DIR, person_name, photo))
        photos.append(photo)

    return Person.insert(id=person_id, name=person_name, photos=photos, role=role_id).execute()


gabo_id = create_person(0, 'gabo', dweller_role_id)
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

cam_latitude = -34.61756707610067
cam_longitude = -58.36823264327735
cam_lat_long_var = -0.000155

for i, area in enumerate(area_ids):
    Camera.insert(alias=areas[i],
                  area_id=area,
                  mac=i,
                  width=width,
                  height=height,
                  framerate=fps,
                  encoding='mp4',
                  latitude=cam_latitude + uniform(-cam_lat_long_var, cam_lat_long_var),
                  longitude=cam_longitude + uniform(-cam_lat_long_var, cam_lat_long_var)
                  ).execute()

print("Training classifier model...")
train_model()
print("Training done!")
