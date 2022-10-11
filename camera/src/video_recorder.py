from logging import getLogger

from picamera import PiCamera

from utils.tracing.src.tracer import get_current_trace_parent
from .local_video import create_local_storage
from .video_metadata import VideoMetadata, ENCODING

QUALITY = 25


class VideoRecorder:

    def __init__(self, camera_id, resolution, framerate, recording_time, tracer, output_queue):
        self.camera = PiCamera(resolution=resolution, framerate=framerate)
        self.camera_id = camera_id
        self.framerate = framerate
        self.resolution = tuple([int(x) for x in resolution.split('x')])
        self.recording_time = recording_time
        self.output_queue = output_queue
        self.tracer = tracer
        create_local_storage()

    def record(self, is_running):
        video_metadata = VideoMetadata(camera_id=self.camera_id,
                                       framerate=self.framerate,
                                       resolution=self.resolution,
                                       duration=self.recording_time)
        self.camera.start_recording(video_metadata.filename, format=ENCODING, quality=QUALITY)

        while is_running():
            with self.tracer.start_as_current_span(video_metadata.id()):
                chunk_trace = get_current_trace_parent()

                with self.tracer.start_as_current_span('camera'):
                    camera_trace = get_current_trace_parent()

                    with self.tracer.start_as_current_span('record'):
                        self.camera.wait_recording(self.recording_time)

                        new_video_metadata = VideoMetadata(camera_id=self.camera_id,
                                                           framerate=self.framerate,
                                                           resolution=self.resolution,
                                                           duration=self.recording_time)
                        self.camera.split_recording(new_video_metadata.filename, format=ENCODING, quality=QUALITY)

                        self.output_queue.put((chunk_trace, camera_trace, video_metadata))
                        video_metadata = new_video_metadata

        self.camera.stop_recording()
        self.camera.close()
