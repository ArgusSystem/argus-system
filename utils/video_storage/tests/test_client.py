from ..src.client import Client

import os.path as path
from io import BytesIO
from filecmp import cmp
from pytest import fixture


@fixture
def bucket_name():
    return 'test-bucket'


@fixture
def object_name():
    return 'test_object'


@fixture
def binary_data():
    return b'argus'


@fixture
def client(bucket_name, object_name):
    client = Client(
        host='localhost',
        port=9500,
        access_key='argus',
        secret_key='panoptes'
    )
    client.make_bucket(bucket_name)

    yield client

    client.remove(bucket_name, object_name)
    client.remove_bucket(bucket_name)


@fixture
def old_filepath(tmp_path, object_name):
    return path.join(tmp_path, f'old_{object_name}.txt')


@fixture
def new_filepath(tmp_path, object_name):
    return path.join(tmp_path, f'new_{object_name}.txt')


def test_file_storage(client, bucket_name, object_name, old_filepath, new_filepath, binary_data):
    with open(old_filepath, 'wb') as file:
        file.write(binary_data)

    client.store_file(bucket_name, object_name, old_filepath)
    client.fetch_file(bucket_name, object_name, new_filepath)

    assert cmp(old_filepath, new_filepath, shallow=False)


def test_storage(client, bucket_name, object_name, binary_data):
    client.store(bucket_name, object_name, BytesIO(binary_data), len(binary_data))
    stored_object = client.fetch(bucket_name, object_name)

    assert binary_data == stored_object
