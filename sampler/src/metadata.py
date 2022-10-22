import cv2

from utils.orm.src.models import Camera, VideoChunk


def get_duration(video_chunk):
    video = cv2.VideoCapture(video_chunk.filepath)

    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / video_chunk.framerate

    video.release()

    return duration


cameras = {}


def store(camera_id, timestamp, duration, samples):
    if camera_id not in cameras:
        cameras[camera_id] = Camera.get(Camera.alias == camera_id)

    camera = cameras[camera_id]

    video_chunk = VideoChunk(camera=camera,
                             timestamp=timestamp,
                             duration=duration,
                             samples=samples)
    video_chunk.save()
