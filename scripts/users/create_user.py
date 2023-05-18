from utils.orm.src.models.user import create
from utils.orm.src.database import connect

connect('argus', 'argus', 5432, 'argus', 'panoptes')

create('argus', 'panoptes', 'argus')
