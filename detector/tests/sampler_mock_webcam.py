import sys
import yaml
import cv2
import os
from utils.video_storage import StorageFactory, StorageType
from utils.events.src.message_clients.rabbitmq import Publisher
from utils.events.src.messages.frame_message import FrameMessage
from utils.events.src.messages.marshalling import encode
from utils.image_processing.src.image_serialization import image_to_bytestring
import time


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("This script takes snapshots from a webcam feed and sends them to a face detector like a sampler would")
        print("")
        print("Usage: ")
        print("python sampler_mock.py time_interval")
        print("--------------------------------")

    else:

        print('[*] Configuring sampler-mock')

        # input
        with open(os.path.dirname(os.path.realpath(__file__)) + "/sampler-mock.yml") as config_file:
            configuration = yaml.safe_load(config_file)
        # print(configuration)

        # Create Storage
        storage = StorageFactory(**configuration['storage']).new(StorageType.VIDEO_FRAMES)

        # Create publiser
        publisher = Publisher.new(**configuration['publisher'])

        # Simulate Sampler -----------------------------------------------

        print('[*] Configuration finished. Starting sampler-mock!')

        # upload video chunk
        # video_chunk = VideoChunk(camera_id="camera_1",
        #                          timestamp=0.0,
        #                          payload="video_chunk".encode())
        # db.add(video_chunk)

        # sample frames
        camera = cv2.VideoCapture(0)
        id_count = 1
        start_time = time.time()
        time_interval = int(sys.argv[1])
        while True:

            # Read frame from Webcam
            ret, image = camera.read()

            elapsed_time = time.time() - start_time
            if elapsed_time >= time_interval:

                # frame = Frame(offset=offset,
                #               video_chunk_id=video_chunk.id)
                # db.add(frame)

                frame_message = FrameMessage(video_chunk="video_chunk_" + str(id_count),
                                             offset="frame_" + str(id_count))

                image_to_bytestring(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                id_count += 1

                publisher.publish(encode(frame_message))

                start_time = time.time()

            # Show image on screen
            cv2.imshow('img', image)

            # Check for exit button 'q'
            ch = cv2.waitKey(1) & 0xFF
            if ch == ord("q"):
                break

        # ----------------------------------------------------------------

        print('[*] sampler-mock stopped!')
