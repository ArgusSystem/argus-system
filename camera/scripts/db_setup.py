from utils.orm.src.database import connect
from utils.orm.src.models import Camera

connect('argus', 'localhost', 5432, 'argus', 'panoptes')

camera = Camera(alias='pi',
                mac=202481588839644,
                width=640,
                height=480,
                framerate=25,
                latitude=0,
                longitude=0)

camera.save()
