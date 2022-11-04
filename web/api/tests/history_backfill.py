from utils.orm.src.database import connect
from utils.orm.src.models import Sighting, Camera, Person
from datetime import datetime


connect('argus', 'localhost', 5432, 'argus', 'panoptes')

person = Person(name='test-person', dni=0)
person.save()

camera_1 = Camera(alias='test-camera-1', mac=-1,
                  width=0, height=0, framerate=0,
                  latitude=-34.585881, longitude=-58.408714)
camera_1.save()

camera_2 = Camera(alias='test-camera-2', mac=-2,
                  width=0, height=0, framerate=0,
                  latitude=-34.585258, longitude=-58.408432)
camera_2.save()

camera_3 = Camera(alias='test-camera-3', mac=-3,
                  width=0, height=0, framerate=0,
                  latitude=-34.585041, longitude=-58.409044)
camera_3.save()

date = int(datetime(2022,10,30,15,55,00).timestamp() * 1000)

Sighting(camera=camera_1,
         person=person,
         start_time=date,
         end_time=date+1000).save()

date += 10000

Sighting(camera=camera_2,
         person=person,
         start_time=date,
         end_time=date+2000).save()

date += 15000

Sighting(camera=camera_3,
         person=person,
         start_time=date,
         end_time=date+3600000).save()

date += 3660000

Sighting(camera=camera_2,
         person=person,
         start_time=date,
         end_time=date+3000).save()

date += 10000

Sighting(camera=camera_1,
         person=person,
         start_time=date,
         end_time=date+1000).save()

