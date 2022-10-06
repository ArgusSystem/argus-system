import cv2
import sys
import yaml
import os
from time import time_ns
from utils.events.src.messages.marshalling import encode
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.video_storage import StorageFactory, StorageType


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("This script records video from a webcam feed and sends it to a Sampler like a Camera would")
        print("")
        print("Usage: ")
        print("python camera_mock.py recording_time ['video_file_path.mp4']")
        print("--------------------------------")

    else:

        print('[*] Configuring camera-mock')

        # input
        with open(os.path.dirname(os.path.realpath(__file__)) + "/camera_mock.yml") as config_file:
            configuration = yaml.safe_load(config_file)

        # Create Storage
        storage = StorageFactory(**configuration['storage']).new(StorageType.VIDEO_CHUNKS)

        # Create publiser
        publisher = Publisher.new(**configuration['publisher'])

        camera_id = 1
        recording_time = int(sys.argv[1])

        if len(sys.argv) == 3:
            input_video = sys.argv[2]
        else:
            input_video = 0
        cap = cv2.VideoCapture(input_video)

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        print("fps: " + str(fps))

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("width: " + str(width) + ", height: " + str(height))

        video_chunk_id = 0

        # Define the codec and create VideoWriter object
        encoding = 'mp4v'
        #fourcc = cv2.VideoWriter_fourcc(*encoding)
        fourcc = cv2.VideoWriter_fourcc(*encoding)
        filename = "output/" + str(camera_id) + "_" + str(video_chunk_id) + ".mp4"
        out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

        frames_written = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                out.write(frame)
                frames_written += 1

                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

            if frames_written == fps * recording_time:
                # Finish recording
                out.release()

                # Create new video chunk message
                message = VideoChunkMessage(camera_id=str(camera_id),
                                            timestamp=time_ns() // 1_000_000,
                                            encoding=encoding,
                                            framerate=fps,
                                            width=width,
                                            height=height)

                # Publish video chunk to file storage
                storage.store(name=str(message), filepath=filename)

                # Send event of new video chunk
                publisher.publish(encode(message))

                # Setup new video recording
                video_chunk_id += 1
                frames_written = 0
                filename = "output/" + str(camera_id) + "_" + str(video_chunk_id) + ".mp4"
                out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

        # Release everything if job is finished
        cap.release()

        cv2.destroyAllWindows()
