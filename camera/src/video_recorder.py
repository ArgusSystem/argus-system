import logging

from picamera import PiCamera
from .local_video import create_local_storage
from .video_metadata import VideoMetadata, ENCODING

QUALITY = 25


class VideoRecorder:

    def __init__(self, resolution, framerate, recording_time, output_queue):
        self.camera = PiCamera(resolution=resolution, framerate=framerate)
        self.framerate = framerate
        self.resolution = resolution
        self.recording_time = recording_time
        self.output_queue = output_queue
        create_local_storage()

    def record(self, is_running):
        video_metadata = VideoMetadata(framerate=self.framerate, resolution=self.resolution)
        self.camera.start_recording(video_metadata.filename, format=ENCODING, quality=QUALITY)

        while is_running():
            self.camera.wait_recording(self.recording_time)

            new_video_metadata = VideoMetadata(framerate=self.framerate, resolution=self.resolution)
            self.camera.split_recording(new_video_metadata.filename, format=ENCODING, quality=QUALITY)

            self.output_queue.put(video_metadata)
            logging.debug(f'New video recorded: {video_metadata.filename}')
            video_metadata = new_video_metadata

        self.camera.stop_recording()
        self.camera.close()
