from ..src.messages.marshalling import encode, decode
from ..src.messages.video_chunk_message import VideoChunkMessage
from ..src.message_clients.rabbitmq.client import Client
from ..src.message_clients.rabbitmq.consumer import Consumer
from ..src.message_clients.rabbitmq.publisher import Publisher
from ..src.message_clients.rabbitmq.management import *

from pytest import fixture
from threading import Event


@fixture
def video_chunk_message():
    return VideoChunkMessage('camera', 0, 'h264', 60, 640, 480)


@fixture
def host():
    return 'localhost'


@fixture
def username():
    return 'argus'


@fixture
def password():
    return 'panoptes'


@fixture
def exchange():
    return 'test-exchange'


@fixture
def routing_key():
    return 'test-routing-key'


@fixture
def queue():
    return 'test-queue'


@fixture
def client(host, username, password, queue, exchange, routing_key):
    client = Client(host, username, password)

    with client.channel() as channel:
        setup_queue(channel, queue)
        setup_exchange(channel, exchange)
        queue_bind(channel, queue, exchange, routing_key)

    yield client

    queue_unbind(channel, queue, exchange, routing_key)
    delete_exchange(channel, exchange)
    delete_queue(channel, queue)
    client.close()


@fixture
def publisher(client, exchange, routing_key):
    return Publisher(
        client=client,
        exchange=exchange,
        routing_key=routing_key
    )


@fixture
def stop_event():
    return Event()


def consume(record, expected_record, stop_event):
    assert expected_record == decode(VideoChunkMessage, record)
    stop_event.set()


@fixture
def consumer(client, queue, video_chunk_message, stop_event):
    return Consumer(
        client=client,
        queue=queue,
        on_message_callback=lambda message: consume(message, video_chunk_message, stop_event),
        stop_event=stop_event
    )


def test_publish_and_consume(publisher, consumer, video_chunk_message):
    publisher.publish(encode(video_chunk_message))
    consumer.start()
