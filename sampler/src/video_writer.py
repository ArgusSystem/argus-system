import os.path as path

from vidgear.gears import WriteGear
from .video_storage import TMP

CONTAINER = 'mp4'


class VideoWriter:

    def __init__(self, camera, timestamp, framerate, width, height):
        self.filename = path.join(TMP, f'{camera}-{timestamp}.{CONTAINER}')

        output_parameters = {
            "-vcodec": "libx264",
            "-movflags": "+dash",
            "-input_framerate": framerate,
            "-output_dimensions": (width, height)
        }

        self._writer = WriteGear(output_filename=self.filename, **output_parameters)

    def write(self, frame):
        self._writer.write(frame)

    def close(self):
        self._writer.close()
