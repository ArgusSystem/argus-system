import os.path

from utils.video_storage import StorageFactory, StorageType

OUTPUT_DIR = '/tmp/scene_of_the_crime/bathroom'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
else:
    print('Directory should not exist!')
    exit(1)

factory = StorageFactory('argus', 9500, 'argus', 'panoptes')

faces_storage = factory.new(StorageType.FRAME_FACES)

count = 0

for o in faces_storage.list():
    faces_storage.fetch(o.object_name, f'{OUTPUT_DIR}/{o.object_name}.jpg')
    count += 1

print(f'{count} files downloaded')
