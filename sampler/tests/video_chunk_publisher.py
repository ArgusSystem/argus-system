#!/usr/bin/python3

from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.events.src.messages.marshalling import encode
from utils.events.src.message_clients.rabbitmq import Publisher

publisher = Publisher.new(host='localhost',
                          username='argus',
                          password='panoptes',
                          exchange='argus',
                          routing_key='video-chunks')

message = VideoChunkMessage(camera_id='test',
                            timestamp=0,
                            encoding='h264',
                            framerate=30,
                            width=640,
                            height=480)

publisher.publish(encode(message))
