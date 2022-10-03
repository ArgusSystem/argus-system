import os
from logging import getLogger

from utils.misc import timer

LOCAL_DIR = '/tmp'


class Frame:

    def __init__(self, offset, filepath):
        self.offset = offset
        self.filepath = filepath


def create_frame(file, frames_dir, sampling_rate):
    return Frame(offset=int(file.split('.')[0]) * sampling_rate,
                 filepath=os.path.join(frames_dir, file))


@timer(getLogger(__name__), 'Sample video')
def sample(video_chunk, sampling_rate):
    frames_dir = os.path.join(LOCAL_DIR, f'{video_chunk.camera_id}-{video_chunk.timestamp}')
    os.mkdir(frames_dir)

    os.system(f'ffmpeg '
              f'-i {video_chunk.filepath} '
              f'-vf fps={sampling_rate} '
              f'{os.path.join(frames_dir, "%d.jpg")} '
              f'> /dev/null 2>&1')

    return frames_dir, [create_frame(file, frames_dir, sampling_rate) for file in os.listdir(frames_dir)]
