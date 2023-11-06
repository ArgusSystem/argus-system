import cv2

from camera.src.video_metadata import VideoMetadata

ENCODING = 'mp4'
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')


class LocalVideoWriterFactory:

    def __init__(self, duration, resolution, framerate):
        self.duration = duration
        self.resolution = tuple(map(int, resolution.split('x')))
        self.framerate = framerate

        print(f'Output resolution: {self.resolution}. '
              f'Output FPS: {self.framerate}')

    def create(self, timestamp):
        return LocalVideoWriter(VideoMetadata(self.duration, timestamp, ENCODING), self.resolution, self.framerate)


class LocalVideoWriter:

    def __init__(self, metadata, resolution, framerate):
        self.metadata = metadata
        self.resolution = resolution
        self.framerate = framerate
        self.video_writer = cv2.VideoWriter(metadata.filename, FOURCC, framerate, resolution)
        self.frames_written = 0

    def write(self, frame):
        if not self.finished():
            resized_frame = cv2.resize(frame, self.resolution, interpolation=cv2.INTER_CUBIC)
            self.video_writer.write(resized_frame)
            self.frames_written += 1

        return self.finished()

    def finished(self):
        return self.frames_written >= self.metadata.duration * self.framerate

    def written(self):
        return self.frames_written // self.framerate

    def close(self):
        self.video_writer.release()
