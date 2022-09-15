from pytest import fixture
from threading import Thread, Event
import filecmp
import os.path as path

from ..src.video_publisher import VideoPublisher
from ..src.video_metadata import VideoMetadata
from ..src.inter_threading_queue import InterThreadingQueue
from ..src.async_task import AsyncTask
from ...utils.events.src.message_clients.rabbitmq import Consumer
from ...utils.events.src.messages.video_chunk_message import VideoChunkMessage
from ...utils.events.src.messages.marshalling import decode
from ...utils.events.src.messages.message_type import MessageType


@fixture
def configuration():
    return {
        'id': 'test-camera',
        'publisher': {
            'host': 'localhost',
            'username': 'argus',
            'password': 'panoptes',
            'exchange': 'argus',
            'routing_key': 'video-chunks'
        },
        'video_storage': {
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
def video_metadata(tmp_path):
    metadata = VideoMetadata(lambda timestamp, encoding: path.join(tmp_path, f'{timestamp}.{encoding}'))

    with open(metadata.filename, 'wb') as file:
        file.write(b'video')

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
    assert expected_record == decode(MessageType.VIDEO_CHUNK, record)
    stop_event.set()


def stop_task(consumer, stop_event):
    stop_event.wait()
    consumer.stop()


@fixture
def consumer(configuration, queue, video_chunk_message, stop_event):
    consumer = Consumer.new(
        host=configuration['publisher']['host'],
        username=configuration['publisher']['username'],
        password=configuration['publisher']['password'],
        queue=queue,
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


def test_publish(video_publisher_task, video_publisher, queue, consumer, video_metadata, video_chunk_message, tmp_path):
    queue.put(video_metadata)

    # Validate that consumer reads the message published
    consumer.start()

    video_chunk_storage_id = str(video_chunk_message)
    video_chunk_filepath = path.join(tmp_path, '')
    video_publisher.storage.fetch(video_chunk_storage_id, video_chunk_filepath)
    assert filecmp.cmp(video_chunk_filepath, video_metadata.filename)
    video_publisher.storage.remove(video_chunk_storage_id)
