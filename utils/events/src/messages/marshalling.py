from .message_type import MessageType
from .video_chunk_message import VideoChunkMessage
from .marshaller import Marshaller


schemas = {
    MessageType.VIDEO_CHUNK: Marshaller(MessageType.VIDEO_CHUNK, VideoChunkMessage)
}

def encode(message):
    if message.mtype in schemas:
        return schemas[message.mtype].encode(message.to_json())

    raise f'No encoder found for {message.mtype}'


def decode(message_type, record):
    if message_type in schemas:
        return schemas[message_type].decode(record)

    raise f'No decoder found for {message_type}'
