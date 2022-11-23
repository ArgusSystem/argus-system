from utils.orm.src.database import connect
from utils.orm.src.models import Camera, VideoChunk
from utils.video_storage import StorageFactory, StorageType

connect('argus', 'localhost', 5432, 'argus', 'panoptes')


camera = Camera(alias='test-camera', mac=-1,
                width=1280, height=720, framerate=30,
                latitude=-34.585881, longitude=-58.408714)
camera.save()

video_chunk = VideoChunk(camera=camera, timestamp=0, duration=1.0, samples=[0, 5, 10, 20, 25])
video_chunk.save()

frames_storage = StorageFactory('argus', 9500, 'argus', 'panoptes').new(StorageType.VIDEO_FRAMES)
frames_storage.store(f'{camera.alias}-{video_chunk.timestamp}-{video_chunk.samples[-1]}',
                     filepath='frames/last_frame.jpeg')

