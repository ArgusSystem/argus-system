#!/usr/bin/env python3

from src.video_processor import VideoProcessor
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer

CONSUMER_KEY = 'consumer'
PUBLISHER_KEY = 'publisher'
SAMPLING_KEY = 'sampling_rate'
STORAGE_KEY = 'storage'


if __name__ == "__main__":
    with run('argus-camera') as application:
        video_processor = VideoProcessor(sampling_rate=application.configuration[SAMPLING_KEY],
                                         storage_configuration=application.configuration[STORAGE_KEY],
                                         publisher_configuration=application.configuration[PUBLISHER_KEY])

        consumer = Consumer.new(**application.configuration[CONSUMER_KEY],
                                on_message_callback=video_processor.process,
                                stop_event=application.stop_event)

        print(f'[*] {application.name} started successfully!')

        consumer.start()

    print(f'[*] {application.name} stopped successfully!')
