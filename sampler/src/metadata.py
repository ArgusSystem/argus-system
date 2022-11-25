import cv2

from utils.orm.src.models import VideoChunk
from utils.orm.src.models.camera import get_camera


def get_duration(video_chunk):
    video = cv2.VideoCapture(video_chunk.filepath)
    framerate = get_camera(video_chunk.camera_id).framerate

    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / framerate

    video.release()

    return duration


def store(camera_id, timestamp, duration, samples):
    camera = get_camera(camera_id)

    video_chunk = VideoChunk(camera=camera,
                             timestamp=timestamp,
                             duration=duration,
                             samples=samples)
    video_chunk.save()
