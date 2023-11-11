import os
from tempfile import gettempdir
from uuid import uuid4


def get_filepath(timestamp, encoding):
    return os.path.join(gettempdir(), f'{timestamp}_{uuid4()}.{encoding}')


def delete_video(filepath):
    os.remove(filepath)


