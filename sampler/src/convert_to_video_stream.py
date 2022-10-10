from .local_video_chunk import LocalVideoChunk, LOCAL_DIR, NULL_DEVICE
from .command import run
import os
from .null_device import null_device

ENCODING = 'mp4'


@timer(getLogger(__name__), 'Convert to DASH video')
def convert(video_chunk):
    filename = f'{video_chunk.camera_id}-{video_chunk.timestamp}.{ENCODING}'
    output_filepath = f'{os.path.join(LOCAL_DIR, filename)}'

    run(f'ffmpeg '
        f'-i {video_chunk.filepath} '
        f'-vcodec libx264 '
        f'-movflags +dash '
        f'-preset ultrafast '
        f'{output_filepath} '
        f'> {null_device()} 2>&1')

    return LocalVideoChunk(camera_id=video_chunk.camera_id,
                           timestamp=video_chunk.timestamp,
                           encoding=ENCODING,
                           framerate=video_chunk.framerate,
                           width=video_chunk.width,
                           height=video_chunk.height,
                           filepath=output_filepath,
                           duration=video_chunk.duration)
