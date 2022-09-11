from .s3_client import S3Client


def get_video_chunks_storage(configuration):
    return S3Client({**configuration, 'bucket': "video-chunks"})


def get_video_frames_storage(configuration):
    return S3Client({**configuration, 'bucket': "video-frames"})