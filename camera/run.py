#!/usr/bin/env python3

from utils.application import run
from camera.src.video_publisher import VideoPublisher
from camera.src.async_task import AsyncTask
from camera.src.inter_threading_queue import InterThreadingQueue
from utils.tracing.src.tracer import get_tracer

ID_KEY = 'id'
PUBLISHER_KEY = 'publisher'
STORAGE_KEY = 'storage'
TRACER_KEY = 'tracer'
VIDEO_RECORDER_KEY = 'video_recorder'


def with_recorder(application_name, create_recorder):
    with run(application_name) as application:
        camera_id = application.configuration[ID_KEY]

        # Used as communication between threads
        queue = InterThreadingQueue()

        # Create tracer
        tracer = get_tracer(**application.configuration[TRACER_KEY], service_name=application.name)

        # Create an asynchronous task to record video
        video_recorder = create_recorder(**application.configuration[VIDEO_RECORDER_KEY],
                                         tracer=tracer,
                                         output_queue=queue)
        recording_task = AsyncTask(video_recorder.record)

        # Create an asynchronous task to publish video
        video_publisher = VideoPublisher(input_queue=queue,
                                         tracer=tracer,
                                         camera_id=camera_id,
                                         publisher_configuration=application.configuration[PUBLISHER_KEY],
                                         storage_configuration=application.configuration[STORAGE_KEY])
        publishing_task = AsyncTask(video_publisher.publish)

        publishing_task.start()
        recording_task.start()

        print(f'[*] {application.name} started successfully!')

        # Wait until the application is stopped
        application.wait()

        # Stop and wait for async tasks
        recording_task.stop()
        publishing_task.stop()

        recording_task.wait()
        publishing_task.wait()

    print(f'[*] {application_name} stopped successfully!')


if __name__ == "__main__":
    from camera.src.video_recorder import VideoRecorder
    with_recorder('argus_camera', VideoRecorder)
