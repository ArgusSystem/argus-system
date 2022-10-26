from utils.orm.src.database import connect
from utils.orm.src.management import create_tables, drop_tables

from utils.orm.src.models.camera import Camera

db = connect('argus', 'localhost', 5432, 'argus', 'panoptes')


class PostgresqlService:

    def __init__(self):
        self.db = connect('argus', 'localhost', 5432, 'argus', 'panoptes')

    def setup(self):
        # Create all the tables from the models
        create_tables(self.db)

        # Create initial camera data for Raspberry PI
        Camera(alias='pi',
               mac=202481588839644,
               width=640,
               height=480,
               framerate=25,
               latitude=-34.61743,
               longitude=-58.36827).save()

        # Create initial camera data for mock
        Camera(alias='camera-mock',
               mac=0,
               width=640,
               height=480,
               framerate=30,
               latitude=-34.61743,
               longitude=-58.36827).save()

    def clean(self):
        drop_tables(self.db)
        self.setup()
