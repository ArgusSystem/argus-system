from queue import Queue

import cv2
import yaml
import os
import shutil
from threading import Thread, Event
from time import time_ns
from utils.events.src.messages.marshalling import encode
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.video_storage import StorageFactory, StorageType
from utils.application.src.signal_handler import SignalHandler
from utils.tracing.src.tracer import get_trace_parent, get_tracer


# This script records video from a webcam feed and sends it to a Sampler like a Camera would
# Usage:
# python camera_mock.py

class WebCamCapture:

    def __init__(self, cap, queue, stop_signal):
        self.cap = cap
        self.queue = queue
        self.stop_signal = stop_signal

    def run(self):
        while cap.isOpened() and not self.stop_signal.is_set():
            ret, frame = self.cap.read()

            if ret:
                self.queue.put(frame)
            else:
                break

        self.cap.release()
        frame_queue.put(None)


if __name__ == "__main__":

    print('[*] Configuring camera-mock')

    # input
    with open(os.path.dirname(os.path.realpath(__file__)) + "/camera_mock.yml") as config_file:
        configuration = yaml.safe_load(config_file)

    # Create tracer
    tracer = get_tracer(**configuration['tracer'], service_name='camera-mock')

    # Create Storage
    storage = StorageFactory(**configuration['storage']).new(StorageType.VIDEO_CHUNKS)

    # Create publisher
    publisher = Publisher.new(**configuration['publisher'])

    camera_id = configuration['camera_id']
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

    video_chunk_id = 0

    # Define the codec and create VideoWriter object
    base_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = base_dir + "/output"
    encoding = 'mp4v'
    fourcc = cv2.VideoWriter_fourcc(*encoding)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Register signal handler
    stop_signal = Event()

    def stop_callback():
        stop_signal.set()

    signal_handler = SignalHandler()
    signal_handler.subscribe(stop_callback)

    frame_queue = Queue()
    webcam = WebCamCapture(cap, frame_queue, stop_signal)
    thread = Thread(target=webcam.run)
    thread.start()

    # Camera loop
    while not stop_signal.is_set():
        # Setup new video chunk recording
        timestamp = time_ns() // 1_000_000
        frames_written = 0
        video_chunk_id += 1
        filename = output_dir + "/" + str(camera_id) + "_" + str(video_chunk_id) + ".mp4"
        out = cv2.VideoWriter(filename, fourcc, fps, resolution)

        with tracer.start_as_current_span('camera'):
            # Record one video chunk
            with tracer.start_as_current_span('record'):
                while frames_written < fps * recording_time:
                    frame = frame_queue.get()

                    if frame is None:
                        break

                    frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
                    out.write(frame)
                    frames_written += 1
                print(frames_written)
                out.release()

            if stop_signal.is_set():
                break

            # Create new video chunk message
            message = VideoChunkMessage(camera_id=camera_id,
                                        timestamp=timestamp,
                                        encoding=encoding,
                                        framerate=fps,
                                        width=width,
                                        height=height,
                                        duration=recording_time,
                                        trace=get_trace_parent())

            # Store video chunk in file storage
            with tracer.start_as_current_span('store'):
                storage.store(name=str(message), filepath=filename)

            # Publish event of new video chunk
            with tracer.start_as_current_span('publish'):
                publisher.publish(encode(message))

            print("Sent a video chunk")

    # Release everything if job is finished
    thread.join()
    cap.release()
    cv2.destroyAllWindows()
    shutil.rmtree(output_dir)
