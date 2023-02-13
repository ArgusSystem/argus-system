import os
import random
import tempfile
from queue import Queue
from threading import Event
from time import time_ns

import cv2
import yaml

from utils.application.src.signal_handler import SignalHandler
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.marshalling import encode
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.orm.src.database import connect
from utils.orm.src.models import Camera
from utils.tracing.src.tracer import get_trace_parent, get_tracer
from utils.video_storage import StorageFactory, StorageType

# This script records video from a webcam feed and sends it to a Sampler like a Camera would
# Usage:
# python camera_mock.py


if __name__ == "__main__":

    print('[*] Configuring camera-mock')

    # input
    with open(os.path.dirname(os.path.realpath(__file__)) + "/development.yml") as config_file:
        configuration = yaml.safe_load(config_file)

    # Create tracer
    tracer = get_tracer(**configuration['tracer'], service_name='camera-mock')

    # Create Storage
    storage = StorageFactory(**configuration['storage']).new(StorageType.VIDEO_CHUNKS)

    # Create publisher
    publisher = Publisher.new(**configuration['publisher'])

    cam_alias_change_frames = configuration['cam_alias_change_frames']
    cam_alias = configuration['cam_alias']
    recording_time = configuration['recording_time']

    use_webcam_feed = configuration['webcam_feed']
    if use_webcam_feed:
        # first available webcam id
        input_video = 0
    else:
        input_video = configuration['video_feed_filepath']
    cap = cv2.VideoCapture(input_video)

    fps = configuration['fps'] if 'fps' in configuration else int(cap.get(cv2.CAP_PROP_FPS))
    print("fps: " + str(fps))

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("native width: " + str(width) + ", native height: " + str(height))

    width = configuration['width']
    height = configuration['height']
    print("output width: " + str(width) + ", output height: " + str(height))
    resolution = (width, height)

    # Define the codec and create VideoWriter object
    base_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = tempfile.gettempdir()
    encoding = 'mp4v'
    fourcc = cv2.VideoWriter_fourcc(*encoding)
    # if not os.path.exists(output_dir):
    #    os.mkdir(output_dir)

    # Register signal handler
    stop_signal = Event()

    def stop_callback():
        stop_signal.set()

    signal_handler = SignalHandler()
    signal_handler.subscribe(stop_callback)

    # Create camera in db
    video_chunk_id = {}

    for i, current_cam_alias in enumerate(cam_alias):
        video_chunk_id[current_cam_alias] = 0

    current_cam_alias = cam_alias[0]
    new_cam_alias = cam_alias[0]
    total_frames = 0

    # Timestamp to  Sunday, November 13, 2022 9:00:18.810 PM
    timestamp_start = 1668373218810

    # Camera loop
    frame = None

    while not stop_signal.is_set():
        # Setup new video chunk recording
        if use_webcam_feed:
            timestamp = time_ns() // 1_000_000
        else:
            timestamp = timestamp_start + int(total_frames * (1.0 / fps) * 1000)
        frames_written = 0
        video_chunk_id[current_cam_alias] += 1
        filename = output_dir + "/" + str(current_cam_alias) + "_" + str(video_chunk_id[current_cam_alias]) + ".mp4"
        out = cv2.VideoWriter(filename, fourcc, fps, resolution)

        with tracer.start_as_current_span('camera'):
            # Record one video chunk
            with tracer.start_as_current_span('record'):
                while frames_written < fps * recording_time:
                    ret, frame = cap.read()

                    if frame is None:
                        break

                    frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
                    out.write(frame)
                    frames_written += 1
                    total_frames += 1

                    new_cam_alias = cam_alias[0]
                    for change_frame in cam_alias_change_frames:
                        if total_frames < change_frame:
                            break
                        else:
                            new_cam_alias = cam_alias[cam_alias_change_frames.index(change_frame)]
                    if current_cam_alias != new_cam_alias:
                        break
                # print(frames_written)
                out.release()

            if stop_signal.is_set():
                break

            # Create new video chunk message
            message = VideoChunkMessage(camera_id=current_cam_alias,
                                        timestamp=timestamp,
                                        encoding=encoding,
                                        duration=recording_time,
                                        trace=get_trace_parent(),
                                        sequence_id=video_chunk_id[current_cam_alias] - 1)

            # Store video chunk in file storage
            with tracer.start_as_current_span('store'):
                storage.store(name=str(message), filepath=filename)

            # Publish event of new video chunk
            with tracer.start_as_current_span('publish'):
                publisher.publish(encode(message))

            current_cam_alias = new_cam_alias
            print("Sent a video chunk: " + str(message))

            # sleep(recording_time/2)

            # input()

            if frame is None:
                break

    cap.release()
    cv2.destroyAllWindows()
    # shutil.rmtree(output_dir)
