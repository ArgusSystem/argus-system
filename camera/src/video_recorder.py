from picamera import PiCamera

from utils.tracing.src.tracer import set_span_in_context
from .local_video import create_local_storage
from .processing_chunk import ProcessingChunk
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
        processing_chunk = None
        previous_record_span = None

        while is_running():
            camera_span = self.tracer.start_span('camera')
            camera_context = set_span_in_context(camera_span)
            record_span = self.tracer.start_span('record', camera_context)

            video_metadata = VideoMetadata(camera_id=self.camera_id,
                                           framerate=self.framerate,
                                           resolution=self.resolution,
                                           duration=self.recording_time)

            if processing_chunk:
                self.camera.split_recording(video_metadata.filename, format=ENCODING, quality=QUALITY)
                self.output_queue.put(processing_chunk)
                previous_record_span.end()
            else:
                self.camera.start_recording(video_metadata.filename, format=ENCODING, quality=QUALITY)

            self.camera.wait_recording(self.recording_time)

            processing_chunk = ProcessingChunk(video_metadata, camera_span, camera_context)
            previous_record_span = record_span

        self.camera.stop_recording()
        self.camera.close()
