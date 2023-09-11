from picamera import PiCamera

from utils.tracing.src.tracer import set_span_in_context
from .processing_chunk import ProcessingChunk
from .video_metadata import VideoMetadata, ENCODING

QUALITY = 25


class VideoRecorder:

    def __init__(self, resolution, framerate, recording_split, tracer, output_queue):
        self.camera = PiCamera(resolution=resolution, framerate=framerate)
        self.recording_split = recording_split
        self.output_queue = output_queue
        self.tracer = tracer

    def record(self, is_running):
        processing_chunk = None
        previous_record_span = None

        while is_running():
            camera_span = self.tracer.start_span('camera')
            camera_context = set_span_in_context(camera_span)
            record_span = self.tracer.start_span('record', camera_context)

            video_metadata = VideoMetadata(duration=self.recording_split)

            if processing_chunk:
                self.camera.split_recording(video_metadata.filename, format=ENCODING, quality=QUALITY)
                self.output_queue.put(processing_chunk)
                previous_record_span.end()
            else:
                self.camera.start_recording(video_metadata.filename, format=ENCODING, quality=QUALITY)

            self.camera.wait_recording(self.recording_split)

            processing_chunk = ProcessingChunk(video_metadata, camera_span, camera_context)
            previous_record_span = record_span

        self.camera.stop_recording()
        self.camera.close()
