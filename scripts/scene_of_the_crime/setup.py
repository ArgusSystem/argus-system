from random import uniform

from utils.orm.src import Area, AreaType, Camera
from utils.orm.src.database import connect

from utils.orm.src.models.user import create as create_user

# Connect to database

connect('argus', 'argus', 5432, 'argus', 'panoptes')


# Create user

user_id = create_user('argus', 'panoptes', 'argus')


# Setup area types

area_type_id = AreaType.insert(name='house').execute()

# Setup areas

areas = ['bath', 'bedroom', 'deck', 'hall', 'kitchen', 'living_room', 'study']
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
