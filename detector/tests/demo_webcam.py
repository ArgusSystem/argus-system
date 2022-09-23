import sys
import cv2
import time
from face_detector_thread import FaceDetectorThread
from detector import FaceDetectorFactory
from utils.image_processing.src.image_serialization import draw_boxes


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

        faceDetectorThread = FaceDetectorThread(faceDetectorObject)
        faceDetectorThread.start()

        # Start webcam
        camera = cv2.VideoCapture(0)
        ret, image = camera.read()
        cv2.imshow('img', image)

        # init FPS calc
        start_time = time.time()
        processed_frames = 0

        rects = []
        while True:

            # Read frame from Webcam
            ret, image = camera.read()

            # Detect faces
            faceDetectorThread.set_image(image)

            if faceDetectorThread.rects_ready():

                # Get bounding boxes
                rects = faceDetectorThread.get_rects()

                # print("Found " + str(len(rects)) + " faces")

                # FPS calc
                processed_frames += 1

            # Draw bounding boxes
            if len(rects) > 0:
                draw_boxes(image, rects, (0, 0, 255))

            # Show image on screen
            cv2.imshow('img', image)

            # Check for exit button 'q'
            ch = cv2.waitKey(1) & 0xFF
            if ch == ord("q"):
                break

        faceDetectorThread.stop()
        faceDetectorThread.join()

        # FPS calc
        total_time = time.time() - start_time
        print("FPS: " + str(processed_frames / total_time))
