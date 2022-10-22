#!/usr/bin/env python3

from src.video_processor import VideoProcessor
from utils.application import run
from utils.events.src.message_clients.rabbitmq import Consumer
from utils.orm.src.database import connect

CONSUMER_KEY = 'consumer'
DB_KEY = 'db'
FRAME_PUBLISHER_KEY = 'frame_publisher'
VIDEO_CHUNK_PUBLISHER_KEY = 'video_chunk_publisher'
SAMPLING_KEY = 'sampling_rate'
STORAGE_KEY = 'storage'
TRACER_KEY = 'tracer'


if __name__ == "__main__":
    with run('argus-sampler') as application:
        configuration = application.configuration

        connect(**configuration[DB_KEY])

        video_processor = VideoProcessor(sampling_rate=configuration[SAMPLING_KEY],
                                         storage_configuration=configuration[STORAGE_KEY],
                                         tracer_configuration=configuration[TRACER_KEY],
                                         frame_publisher_configuration=configuration[FRAME_PUBLISHER_KEY],
                                         video_chunk_publisher_configuration=configuration[VIDEO_CHUNK_PUBLISHER_KEY])

        consumer = Consumer.new(**configuration[CONSUMER_KEY],
                                on_message_callback=video_processor.process,
                                stop_event=application.stop_event)

        print(f'[*] {application.name} started successfully!')

        consumer.start()

    print(f'[*] {application.name} stopped successfully!')
