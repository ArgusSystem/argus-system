from ..src.messages.marshalling import encode, decode
from ..src.messages.message_type import MessageType
from ..src.messages.video_chunk_message import VideoChunkMessage

def test_video_chunk():
    message = VideoChunkMessage('camera', 0)
    record = encode(MessageType.VIDEO_CHUNK, message)
    assert message == decode(MessageType.VIDEO_CHUNK, record)

