from .s3_client import S3Client


def get_raw_storage(configuration):
    return S3Client({**configuration, 'bucket': "raw-video-chunks"})


def get_processed_storage(configuration):
    return S3Client({**configuration, 'bucket': "processed-video-chunks"})