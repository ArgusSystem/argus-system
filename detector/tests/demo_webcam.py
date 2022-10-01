import sys
import cv2
import time
from detector import FaceDetectorFactory
from utils.image_processing.src.image_serialization import draw_boxes
from multiprocessing.pool import ThreadPool


def detect_faces(detector, image):
    return detector.detect_face_image(image)


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("This script receives a face detectory type and displays a webcam feed with overlaid face detection.")
        print("Press 'q' to quit.")
        print("")
        print("Usage: ")
        print("python demo_webcam.py ['tensorflow_mtcnn | mvds_ssd' | 'mvds_ssd_longrange' | 'mvds_mtcnn' | 'caffe_mtcnn']")
        print("--------------------------------")

    else:

        # Create Face Detector
        face_detector_type = sys.argv[1]
        faceDetectorObject = FaceDetectorFactory.build_by_type(face_detector_type)

        # Start webcam
        camera = cv2.VideoCapture(0)
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
