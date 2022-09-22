#!/usr/bin/env python3

from src.video_processor import VideoProcessor
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer

CONSUMER_KEY = 'consumer'

if __name__ == "__main__":
    with run('argus-camera') as application:
        video_processor = VideoProcessor()

        consumer = Consumer.new(**application.configuration[CONSUMER_KEY],
                                on_message_callback=video_processor.process,
                                stop_event=application.stop_event)

        print(f'[*] {application.name} started successfully!')

        consumer.start()

    print(f'[*] {application.name} stopped successfully!')
