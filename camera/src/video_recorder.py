from picamera import PiCamera
from .local_video import create_local_storage
from .video_metadata import VideoMetadata, FORMAT


class VideoRecorder:

    def __init__(self, resolution, framerate, recording_time, output_queue):
        self.camera = PiCamera(resolution=resolution, framerate=framerate)
        self.recording_time = recording_time
        self.output_queue = output_queue
        create_local_storage()

    def record(self, is_running):
        video_metadata = VideoMetadata()
        self.camera.start_recording(video_metadata.filename, format=FORMAT, quality=25)

        while is_running():
            self.camera.wait_recording(self.recording_time)
            self.output_queue.put(video_metadata)

            video_metadata = VideoMetadata()
            self.camera.split_recording(video_metadata.filename, format=FORMAT, quality=25)

        self.camera.stop_recording()
        self.camera.close()
