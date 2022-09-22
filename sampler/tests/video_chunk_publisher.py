#!/usr/bin/python3

from big_fiubrother_core.messages import VideoChunkMessage
from big_fiubrother_core.message_clients.rabbitmq import Publisher


class VideoChunkPublisher:

    def __init__(self, configuration):
        self.publisher = Publisher(configuration)

    def publish(self, video_chunk_path):
        with open(video_chunk_path, 'rb') as file:
            buffer = file.read()

        message = VideoChunkMessage(camera_id='TEST_CAMERA',
                                    timestamp=0.0,
                                    payload=buffer)

        self.publisher.publish(message)

        return message

configuration = {
  # 'host': '192.168.1.28',
  'host': 'localhost',
  'username': 'fiubrother',
  'password': 'alwayswatching',
  'exchange': 'fiubrother',
  'routing_key': 'video_chunks'
}

publisher = VideoChunkPublisher(configuration)

publisher.publish('../tmp/CAMERA_1_05-10-2019||22:32:47.794347.h264')