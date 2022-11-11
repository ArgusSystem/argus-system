from utils.orm.src.database import connect
from utils.orm.src.management import create_tables, drop_tables

from utils.orm.src.models import Camera, Person

#db = connect('argus', 'localhost', 5432, 'argus', 'panoptes')


class PostgresqlService:

    def __init__(self, host):
        self.db = connect('argus', host, 5432, 'argus', 'panoptes')

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

        #Person.insert(id=0, name='gonza', dni='33333333').execute()
        #Person(name='gabo', dni='11111111').save()
        #Person(name='edu', dni='22222222').save()

        # -- ROPE (el orden de los ids es importante)
        Person.insert(id=0, name='brandon_shaw', dni='33333333').execute()
        Person.insert(id=1, name='janet_walker', dni='33333333').execute()
        Person.insert(id=2, name='kenneth_lawrence', dni='33333333').execute()
        Person.insert(id=3, name='mrs_anita_atwater', dni='33333333').execute()
        Person.insert(id=4, name='mrs_wilson', dni='33333333').execute()
        Person.insert(id=5, name='mr_henry_kentley', dni='33333333').execute()
        Person.insert(id=6, name='phillip_morgan', dni='33333333').execute()
        Person.insert(id=7, name='ruperts_cadell', dni='33333333').execute()


    def clean(self):
        drop_tables(self.db)
        #self.setup()
