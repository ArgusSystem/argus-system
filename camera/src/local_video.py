import os

TMP = 'tmp'


def create_local_storage():
    if not os.path.exists(TMP):
        os.mkdir(TMP)


def get_filepath(timestamp, encoding):
    return os.path.join(TMP, f'{timestamp}.{encoding}')


def delete_video(filepath):
    os.remove(filepath)


