import os
from math import ceil, floor

from utils.orm.src.models.camera import get_camera
from .command import run
from .local_video_chunk import LOCAL_DIR, NULL_DEVICE


class Frame:

    def __init__(self, offset, timestamp, filepath):
        self.offset = offset
        self.timestamp = timestamp
        self.filepath = filepath


def get_frames(frames_dir, video_timestamp, framerate, sampling_rate):
    files = os.listdir(frames_dir)
    files.sort(key=lambda f: int(f.split('.')[0]))

    in_between_frames = framerate / sampling_rate
    offset = in_between_frames / 2

    frames = []

    for file in files:
        # Count offsets from 0 to N-1
        offset = ceil(offset)
        frame = Frame(offset=offset,
                      timestamp=floor(video_timestamp + offset * (1000 / framerate)),
                      filepath=os.path.join(frames_dir, file))
        frames.append(frame)
        offset += in_between_frames

    return frames


def sample(video_chunk, sampling_rate):
    frames_dir = os.path.join(LOCAL_DIR, f'{video_chunk.camera_id}-{video_chunk.timestamp}')

    if not os.path.exists(frames_dir):
        os.mkdir(frames_dir)

    run(f'ffmpeg -i {video_chunk.filepath} '
        f'-vf fps={sampling_rate} '
        f'{os.path.join(frames_dir, "%d.jpg")} '
        f'> {NULL_DEVICE} 2>&1')

    framerate = get_camera(video_chunk.camera_id).framerate

    return frames_dir, get_frames(frames_dir, video_chunk.timestamp, framerate, sampling_rate)
