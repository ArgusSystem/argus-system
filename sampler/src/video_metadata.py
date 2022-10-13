import cv2


def get_duration(video_chunk):
    video = cv2.VideoCapture(video_chunk.filepath)

    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / video_chunk.framerate

    video.release()

    return duration
