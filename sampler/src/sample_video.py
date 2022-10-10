import os
from .command import run
import tempfile
from logging import getLogger

from utils.tracing import timer
from .null_device import null_device

LOCAL_DIR = tempfile.gettempdir()


class Frame:

    def __init__(self, offset, filepath):
        self.offset = offset
        self.filepath = filepath


def create_frame(file, frames_dir, frames_between_samples):
    # IMPORTANTE: la logica de calcular los offsets tiene que ser la misma que en el Web server
    offset = round(frames_between_samples / 2) + (int(file.split('.')[0]) - 1) * frames_between_samples
    return Frame(offset=offset, filepath=os.path.join(frames_dir, file))


def sample(video_chunk, sampling_rate):
    frames_dir = os.path.join(LOCAL_DIR, f'{video_chunk.camera_id}-{video_chunk.timestamp}')

    if not os.path.exists(frames_dir):
        os.mkdir(frames_dir)

    frames_between_samples = round(video_chunk.framerate / sampling_rate)
    ffmpeg_command = f'ffmpeg -i {video_chunk.filepath} ' \
                     f'-vf fps={sampling_rate} ' \
                     f'{os.path.join(frames_dir, "%d.jpg")} ' \
                     f'> {null_device()} 2>&1'
    os.system(ffmpeg_command)

    return frames_dir, [create_frame(file, frames_dir, frames_between_samples) for file in os.listdir(frames_dir)]
