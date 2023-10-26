import sys
import cv2
import time
import os
from detector import FaceDetectorFactory
from utils.image_processing.src.image_serialization import draw_boxes
from multiprocessing.pool import ThreadPool
from utils.application.src.configuration import load_configuration

# This runs live face detection on a webcam feed using the specified face detector.
# It then shows the feed on screen, with drawn bounding boxes.

# Run this script from argus-system/
# Configure by changing ./demo_webcam.yml


def detect_faces(detector, image):
    return detector.detect_face_image(image)


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.realpath(__file__))
    configuration = load_configuration(base_dir + '/demo_webcam.yml')

    # Create Face Detector
    face_detector_type = configuration['face_detector']
    faceDetectorObject = FaceDetectorFactory.build_by_type(face_detector_type)

    # Start webcam
    use_webcam_feed = configuration['webcam_feed']
    if use_webcam_feed:
        # first available webcam id
        input_video = 0
    else:
        input_video = configuration['video_feed_filepath']
    camera = cv2.VideoCapture(input_video)
    ret, image = camera.read()
    cv2.imshow('img', image)

    # init FPS calc
    start_time = time.time()
    processed_frames = 0

    pool = ThreadPool(processes=1)
    async_result = None
    rects = []
    first_frame = True

    while True:

        # Read frame from Webcam
        ret, image = camera.read()

        if image is None:
            break

        width = int(image.shape[1])
        height = int(image.shape[0])
        dim = (width * 2, height * 2)
        #image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        if async_result is None:
            async_result = pool.apply_async(detect_faces, (faceDetectorObject, image))
        elif async_result.ready():
            processed_frames += 1
            if first_frame:
                start_time = time.time()
                processed_frames = 0
                first_frame = False
            rects = async_result.get()
            async_result = pool.apply_async(detect_faces, (faceDetectorObject, image))

        # Draw bounding boxes
        if len(rects) > 0:
            draw_boxes(image, rects, (0, 0, 255))

        # Show image on screen
        cv2.imshow('img', image)

        # Check for exit button 'q'
        ch = cv2.waitKey(1) & 0xFF
        if ch == ord("q"):
            break

    pool.close()
    pool.terminate()

    # FPS calc
    total_time = time.time() - start_time
    print("FPS: " + str(processed_frames / total_time))
