import os

TMP = '/tmp'


def get_filepath(timestamp, encoding):
    return os.path.join(TMP, f'{timestamp}.{encoding}')


def delete_video(filepath):
    os.remove(filepath)


