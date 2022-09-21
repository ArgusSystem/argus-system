from pytest import fixture
from threading import Thread, Event
import filecmp
import os.path as path

from ..src.video_publisher import VideoPublisher
from ..src.video_metadata import VideoMetadata
from ..src.inter_threading_queue import InterThreadingQueue
from ..src.async_task import AsyncTask
from utils.events.src.message_clients.rabbitmq import Consumer
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.events.src.messages.marshalling import decode
from utils.events.src.messages.message_type import MessageType


@fixture
def configuration():
    return {
        'id': 'test-camera',
        'publisher': {
            'host': 'localhost',
            'username': 'argus',
            'password': 'panoptes',
            'exchange': 'argus',
            'routing_key': ''
        },
        'storage': {
            'host': 'localhost',
            'port': 9500,
            'access_key': 'argus',
            'secret_key': 'panoptes'
        }
    }


@fixture
def queue():
    return InterThreadingQueue()


@fixture
def video_bytes():
    return b'video'


@fixture
def video_metadata(tmp_path, video_bytes):
    metadata = VideoMetadata(lambda timestamp, encoding: path.join(tmp_path, f'{timestamp}.{encoding}'))

    with open(metadata.filename, 'wb') as file:
        file.write(video_bytes)

    return metadata


@fixture
def video_chunk_message(configuration, video_metadata):
    return VideoChunkMessage(configuration['id'], video_metadata.timestamp)


@fixture
def video_publisher(configuration, queue):
    return VideoPublisher(queue, configuration)


@fixture
def stop_event():
    return Event()


def consume(record, expected_record, stop_event):
    actual_record = decode(MessageType.VIDEO_CHUNK, record)
    assert expected_record == actual_record
    stop_event.set()


def stop_task(consumer, stop_event):
    stop_event.wait()
    consumer.stop()


@fixture
def consumer(configuration, video_chunk_message, stop_event):
    consumer = Consumer.new(
        host=configuration['publisher']['host'],
        username=configuration['publisher']['username'],
        password=configuration['publisher']['password'],
        queue='video-chunks',
        on_message_callback=lambda message: consume(message, video_chunk_message, stop_event)
    )

    stopping_thread = Thread(target=lambda: stop_task(consumer, stop_event))
    stopping_thread.start()

    yield consumer

    stopping_thread.join()


@fixture
def video_publisher_task(video_publisher, video_metadata):
    task = AsyncTask(video_publisher.publish)
    task.start()

    yield task

    task.stop()
    task.wait()


def test_publish(video_publisher_task, video_publisher, queue, consumer, video_chunk_message, tmp_path, video_metadata,
                 video_bytes):
    queue.put(video_metadata)

    # Validate that consumer reads the message published
    consumer.start()

    # Validate the file was stored contains the same information
    video_chunk_storage_id = str(video_chunk_message)
    video_chunk_filepath = path.join(tmp_path, 'stored_file.txt')
    video_publisher.storage.fetch(str(video_chunk_message), video_chunk_filepath)

    with open(video_chunk_filepath, 'rb') as file:
        actual_bytes = file.read()

    assert actual_bytes == video_bytes

    video_publisher.storage.remove(video_chunk_storage_id)
