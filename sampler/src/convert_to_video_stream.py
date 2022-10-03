from .local_video_chunk import LocalVideoChunk, LOCAL_DIR
from logging import getLogger
from utils.tracing import timer
import os

ENCODING = 'mp4'


@timer(getLogger(__name__), 'Convert to DASH video')
def convert(video_chunk):
    filename = f'{video_chunk.camera_id}-{video_chunk.timestamp}.{ENCODING}'
    output_filepath = f'{os.path.join(LOCAL_DIR, filename)}'

    os.system(f'ffmpeg '
              f'-i {video_chunk.filepath} '
              f'-vcodec libx264 '
              f'-movflags +dash '
              f'-r {video_chunk.framerate} '
              f'-preset ultrafast '
              f'{output_filepath} '
              f'> /dev/null 2>&1')

    return LocalVideoChunk(camera_id=video_chunk.camera_id,
                           timestamp=video_chunk.timestamp,
                           encoding=ENCODING,
                           framerate=video_chunk.framerate,
                           width=video_chunk.width,
                           height=video_chunk.height,
                           filepath=output_filepath)
