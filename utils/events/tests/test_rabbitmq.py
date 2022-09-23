from ..src.messages.marshalling import encode, decode
from ..src.messages.video_chunk_message import VideoChunkMessage
from ..src.message_clients.rabbitmq.client import Client
from ..src.message_clients.rabbitmq.consumer import Consumer
from ..src.message_clients.rabbitmq.publisher import Publisher
from ..src.message_clients.rabbitmq.management import *

from pytest import fixture
from threading import Thread, Event


@fixture
def video_chunk_message():
    return VideoChunkMessage('camera', 0)


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
    assert expected_record == decode(MessageType.VIDEO_CHUNK, record)
    stop_event.set()


def stop_task(consumer, stop_event):
    stop_event.wait()
    consumer.stop()


@fixture
def consumer(client, queue, video_chunk_message, stop_event):
    consumer = Consumer(
        client=client,
        queue=queue,
        on_message_callback=lambda message: consume(message, video_chunk_message, stop_event)
    )

    stopping_thread = Thread(target=lambda: stop_task(consumer, stop_event))
    stopping_thread.start()

    yield consumer

    stopping_thread.join()


# Will process only the message published
def test_publish_and_consume(publisher, consumer, video_chunk_message):
    publisher.publish(encode(video_chunk_message))
    consumer.start()
