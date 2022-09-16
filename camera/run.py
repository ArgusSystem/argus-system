#!/usr/bin/env python3

from utils.application import run
from src.video_recorder import VideoRecorder
from src.video_publisher import VideoPublisher
from src.async_task import AsyncTask
from src.inter_threading_queue import InterThreadingQueue


VIDEO_RECORDER_KEY = 'video_recorder'


if __name__ == "__main__":
    with run('argus-camera') as application:
        # Used as communication between threads
        queue = InterThreadingQueue()

        # Create an asynchronous task to record video
        video_recorder = VideoRecorder(**application.configuration[VIDEO_RECORDER_KEY], output_queue=queue)
        recording_task = AsyncTask(video_recorder.record)

        # Create an asynchronous task to publish video
        video_publisher = VideoPublisher(queue, application.configuration)
        publishing_task = AsyncTask(video_publisher.publish)

        print(f'[*] {application.name} started successfully!')

        # Wait until the application is stopped
        application.wait()

        # Stop and wait for async tasks
        recording_task.stop()
        publishing_task.stop()

        recording_task.wait()
        publishing_task.wait()

    print(f'[*] {application.name} stopped successfully!')


