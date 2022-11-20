# Create initial camera data for Raspberry PI
from utils.orm.src import Camera
from utils.orm.src.database import connect

connect('argus', 'argus', 5432, 'argus', 'panoptes')


Camera(alias='pi',
       mac=202481588839644,
       width=640,
       height=480,
       framerate=25,
       latitude=-34.61743,
       longitude=-58.36827).save()
