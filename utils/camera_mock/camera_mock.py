import cv2
import sys
import yaml
import os
import shutil
from time import time_ns
from utils.events.src.messages.marshalling import encode
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.video_storage import StorageFactory, StorageType
from utils.application.src.signal_handler import SignalHandler
from utils.tracing.src.tracer import get_current_trace_parent, get_tracer, get_context
from camera.src.video_metadata import VideoMetadata


# This script records video from a webcam feed and sends it to a Sampler like a Camera would
# Usage:
# python camera_mock.py


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

    fps = int(cap.get(cv2.CAP_PROP_FPS))
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
    stop_signal_sent = False

    def stop_callback():
        global stop_signal_sent
        stop_signal_sent = True

    signal_handler = SignalHandler()
    signal_handler.subscribe(stop_callback)

    # Camera loop
    while not stop_signal_sent:

        # Setup new video chunk recording
        timestamp = time_ns() // 1_000_000
        frames_written = 0
        video_chunk_id += 1
        filename = output_dir + "/" + str(camera_id) + "_" + str(video_chunk_id) + ".mp4"
        out = cv2.VideoWriter(filename, fourcc, fps, resolution)
        trace_chunk_id = f'{camera_id}-{timestamp}'

        # Record and publish one video chunk
        with tracer.start_as_current_span(trace_chunk_id):
            chunk_trace = get_current_trace_parent()

            with tracer.start_as_current_span('camera'):

                # Record one video chunk
                with tracer.start_as_current_span('record'):
                    while cap.isOpened() and not stop_signal_sent:
                        ret, frame = cap.read()
                        if ret:
                            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
                            out.write(frame)
                            frames_written += 1

                            # cv2.imshow('frame', frame)
                            # if cv2.waitKey(1) & 0xFF == ord('q'):
                            #     break
                        else:
                            break

                        if frames_written == fps * recording_time:
                            # Finish recording
                            out.release()
                            break

                if stop_signal_sent:
                    out.release()
                    break

                # Create new video chunk message
                message = VideoChunkMessage(camera_id=camera_id,
                                            timestamp=timestamp,
                                            encoding=encoding,
                                            framerate=fps,
                                            width=width,
                                            height=height,
                                            duration=recording_time,
                                            trace=chunk_trace)

                # Store video chunk in file storage
                with tracer.start_as_current_span('store'):
                    storage.store(name=str(message), filepath=filename)

                # Publish event of new video chunk
                with tracer.start_as_current_span('publish'):
                    publisher.publish(encode(message))

                print("Sent a video chunk")

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()
    shutil.rmtree(output_dir)
