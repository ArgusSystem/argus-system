# Video storage module

The *video storage* module handles the storage of binary information, more specifically video chunks and frames. Currently, 
all this data is stored in an S3 storage, divided in two buckets respectively:
- *video-chunks*
- *video-frames*

## Usage

```python
from utils.video_storage.src.storage import get_video_chunks_storage, get_video_frames_storage

# Split video into frame
def split_video(filepath):
    return ['frame1', 'frame2', 'frame3']

# Configuration for S3 storage
configuration = {
    'host': 'localhost',
    'port': 9500,
    'access_key': 'fiubrother',
    'secret_key': '1234'
}

# Fetch file with id from video chunks storage. Store it in filepath.
video_chunk_storage = get_video_chunks_storage(configuration)
video_chunk_storage.retrieve_file('id', 'filepath')


video_frames_storage = get_video_frames_storage(configuration)

for frame in split_video('filepath'):
    # Store frames in filepath into the frames storage
    video_frames_storage.store_file('id', frame)
```