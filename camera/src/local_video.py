import os

TMP = 'tmp'


def create_local_storage():
    if not os.path.exists(TMP):
        os.mkdir(TMP)


def get_filepath(timestamp, video_format):
    return os.path.join(TMP, f'{timestamp}.{video_format}')


def delete_video(filepath):
    os.remove(filepath)


