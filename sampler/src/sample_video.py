import os
from .local_video_chunk import LOCAL_DIR, NULL_DEVICE
from .command import run


class Frame:

    def __init__(self, offset, filepath):
        self.offset = offset
        self.filepath = filepath


def create_frame(file, frames_dir, sampling_rate):
    return Frame(offset=int(file.split('.')[0]) * sampling_rate,
                 filepath=os.path.join(frames_dir, file))


def sample(video_chunk, sampling_rate):
    frames_dir = os.path.join(LOCAL_DIR, f'{video_chunk.camera_id}-{video_chunk.timestamp}')

    if not os.path.exists(frames_dir):
        os.mkdir(frames_dir)

    run(f'ffmpeg '
        f'-i {video_chunk.filepath} '
        f'-vf fps={sampling_rate} '
        f'{os.path.join(frames_dir, "%d.jpg")} '
        f'> {NULL_DEVICE} 2>&1')

    return frames_dir, [create_frame(file, frames_dir, sampling_rate) for file in os.listdir(frames_dir)]
