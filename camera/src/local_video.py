import os
from tempfile import gettempdir


def get_filepath(timestamp, encoding):
    return os.path.join(gettempdir(), f'{timestamp}.{encoding}')


def delete_video(filepath):
    os.remove(filepath)


