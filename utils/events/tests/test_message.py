from ..src.messages.marshalling import encode, decode
from ..src.messages.video_chunk_message import VideoChunkMessage

from pytest import fixture


@fixture
def message():
    return VideoChunkMessage('camera', 0, 'h264', 60, 640, 480)


def test_video_chunk(message):
    record = encode(message)
    assert message == decode(VideoChunkMessage, record)
