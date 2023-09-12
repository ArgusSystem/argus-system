from time import time_ns

from camera.run import with_recorder
from camera.src.processing_chunk import ProcessingChunk
from scripts.signaller import signal_sigint
from utils.tracing.src.tracer import set_span_in_context
from scripts.local_video_capture import LocalVideoCapture
from scripts.local_video_writer import LocalVideoWriterFactory


class LocalVideoStreamer:

    def __init__(self, filepath, resolution, framerate, recording_split, tracer, output_queue):
        self.video_capture = LocalVideoCapture(filepath)
        self.video_writer_factory = LocalVideoWriterFactory(recording_split, resolution, framerate)

        self.tracer = tracer
        self.output_queue = output_queue

    def record(self, is_running):
        not_eof = True
        timestamp = (time_ns() // 1_000_000_000) * 1_000  # Time in MS truncated

        while not_eof and is_running():
            camera_span = self.tracer.start_span('camera')
            camera_context = set_span_in_context(camera_span)

            with self.tracer.start_as_current_span('record', camera_context):
                video_writer = self.video_writer_factory.create(timestamp)

                finished = False

                while not_eof and not finished and not video_writer.finished():
                    not_eof, frame = self.video_capture.read()

                    if not_eof:
                        finished = video_writer.write(frame)

                video_writer.close()

                if video_writer.frames_written > 0:
                    self.output_queue.put(ProcessingChunk(video_writer.metadata, camera_span, camera_context))

                    timestamp += video_writer.written() * 1_000

        self.video_capture.close()

        signal_sigint()


if __name__ == "__main__":
    with_recorder('argus-video-streamer', LocalVideoStreamer)
