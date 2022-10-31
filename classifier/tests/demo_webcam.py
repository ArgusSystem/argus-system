import sys
import cv2
import time
from classifier import FaceEmbedderFactory
from classifier.src.classifier_support_vector import SVClassifier
from utils.image_processing.src.image_serialization import draw_boxes
from multiprocessing.pool import ThreadPool
from detector import FaceDetectorFactory
import os
# from sklearn.preprocessing import Normalizer


confidence_t = 0.99
required_size = (160, 160)
# l2_normalizer = Normalizer('l2')


def get_face(img, box):
    #print(box)
    x1, y1, x2, y2 = [int(x) for x in box]
    #x1, y1 = abs(x1), abs(y1)
    #x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)


def detect_raw(img, detector, encoder, classifier):
    boxes = detector.detect_face_image(img.copy())
    results = []
    for bbox in boxes:
        res = {}
        face, pt_1, pt_2 = get_face(img, bbox[:4])
        encoding = encoder.get_embedding_mem(face)
        #encoding = l2_normalizer.transform(encoding.reshape(1, -1))[0]
        name = 'unknown'
        pred_index, pred_prob = classifier.predict(encoding)
        pred_name = classifier.get_name(pred_index)
        if pred_prob > recognition_t:
            name = pred_name
        res['name'] = name
        res['prob'] = pred_prob
        res['pt_1'] = pt_1
        res['pt_2'] = pt_2
        results.append(res)
    return results


def raw_to_frame(img, results):
    for res in results:
        name = res['name']
        prob = res['prob']
        pt_1 = res['pt_1']
        pt_2 = res['pt_2']
        if name == 'unknown':
            cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        else:
            cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
            cv2.putText(img, name + f'__{prob:.2f}', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 200, 200), 2)
    return img


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("This script receives a face embedder type and displays a webcam feed with overlaid face detection and classification.")
        print("Press 'q' to quit.")
        print("")
        print("Usage: ")
        print("python demo_webcam.py 'face_detector_type' 'face_embedder_type' 'face_classifier.pkl' 'recognition_treshold'")
        print("--------------------------------")

    else:
        base_dir = os.path.dirname(os.path.realpath(__file__))

        # Create Face Detector
        face_detector_type = sys.argv[1]
        face_detector = FaceDetectorFactory.build_by_type(face_detector_type)

        # Create Face Embedder
        face_embedder_type = sys.argv[2]
        face_embedder = FaceEmbedderFactory.build_by_type(face_embedder_type)

        # Create Face Classifier
        face_classifier = SVClassifier.load(sys.argv[3])

        # Recognition Treshold
        recognition_t = float(sys.argv[4])

        # Start webcam
        camera = cv2.VideoCapture(0)

        # init FPS calc
        start_time = time.time()
        processed_frames = 0

        pool = ThreadPool(processes=1)
        async_result = None
        results = []
        first_frame = True

        while True:

            # Read frame from Webcam
            ret, image = camera.read()

            if async_result is None:
                async_result = pool.apply_async(detect_raw, (image, face_detector, face_embedder, face_classifier))
            elif async_result.ready():
                processed_frames += 1
                if first_frame:
                    start_time = time.time()
                    processed_frames = 0
                    first_frame = False
                results = async_result.get()
                async_result = pool.apply_async(detect_raw, (image.copy(), face_detector, face_embedder, face_classifier))
            image = raw_to_frame(image, results)

            # Show image on screen
            cv2.imshow('img', image)

            # Check for exit button 'q'
            ch = cv2.waitKey(1) & 0xFF
            if ch == ord("q"):
                break

        # FPS calc
        total_time = time.time() - start_time
        print("FPS: " + str(processed_frames / total_time))
