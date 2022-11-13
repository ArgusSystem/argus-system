from os import listdir, path

from utils.orm.src.database import connect
from utils.orm.src.models import Person
from utils.video_storage import StorageFactory, StorageType

#
# Setup persons and cameras for Friends
#

people_storage = StorageFactory('localhost', 9500, 'argus', 'panoptes').new(StorageType.PEOPLE)

connect('argus', 'localhost', 5432, 'argus', 'panoptes')

PEOPLE_DIR = 'people'

for i, person_name in enumerate(sorted(listdir(PEOPLE_DIR))):
    photos = []

    for photo in listdir(path.join(PEOPLE_DIR, person_name)):
        people_storage.store(name=photo, filepath=path.join(PEOPLE_DIR, person_name, photo))
        photos.append(photo)

    Person.insert(id=i, name=person_name, photos=photos).execute()
