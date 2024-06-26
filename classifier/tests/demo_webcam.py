import sys
import cv2
import time
from classifier import FaceEmbedderFactory, FaceClassifierFactory
from detector import FaceDetectorFactory
from utils.application.src.configuration import load_configuration
from multiprocessing.pool import ThreadPool
import os
# from sklearn.preprocessing import Normalizer

# This scipt uses the specified detector, embedder and classifier to perform real time face classification
# on a webcam feed, and displays that feed on screen with bounding boxes and labels

# Run this script from argus-system/
# Configure by changing ./demo_webcam.yml

# If playing a video instead of a webcam feed:
# Press SPACEBAR to pause the video
# Press F to advance and process one frame
# Press S to skip 100 frames
# Press W to skip 1000 frames

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


def write_text_with_background(img, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    (text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=thickness)[0]
    text_offset_x = 0
    text_offset_y = 25
    box_coords = (
    (text_offset_x - 2, text_offset_y - text_height - 2), (text_offset_x + text_width + 2, text_offset_y + 2))
    cv2.rectangle(img, box_coords[0], box_coords[1], (255, 255, 255), cv2.FILLED)
    cv2.putText(img, text, (text_offset_x, text_offset_y), font, font_scale, (0, 0, 0), thickness)
    return img


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.realpath(__file__))
    configuration = load_configuration(base_dir + '/demo_webcam.yml')

    # Create Face Detector
    face_detector_type = configuration['face_detector']
    face_detector = FaceDetectorFactory.build_by_type(face_detector_type)

    # Create Face Embedder
    face_embedder_type = configuration['face_embedder']
    face_embedder = FaceEmbedderFactory.build_by_type(face_embedder_type)

    # Create Face Classifier
    face_classifier = FaceClassifierFactory.build(configuration['face_classifier'])

    # Recognition Treshold
    recognition_t = float(configuration['threshold'])

    # Start webcam
    video_path = configuration['video_feed_filepath']
    cam_index = 0
    if video_path:
        cam_index = video_path
    camera = cv2.VideoCapture(cam_index)

    # Cam id test
    cam_id_change_frames = configuration['cam_id_change_frames']
    cam_ids = configuration['cam_ids']

    # init FPS calc
    start_time = time.time()
    processed_frames = 0

    pool = ThreadPool(processes=1)
    async_result = None
    results = []
    first_frame = True
    paused = False
    process_one_frame = False
    frame_number = 0

    while True:

        if not paused or process_one_frame:
            # Read frame from Webcam
            ret, image = camera.read()
            if image is None:
                break
            frame_number += 1

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
            camera_id = cam_ids[0]
            for change_frame in cam_id_change_frames:
                if frame_number <= change_frame:
                    break
                else:
                    camera_id = cam_ids[cam_id_change_frames.index(change_frame)]
            image = write_text_with_background(image, camera_id)
            cv2.imshow('img', image)

        # Check for exit button 'q'
        process_one_frame = False
        ch = cv2.waitKey(1) & 0xFF
        if ch == ord("q"):
            break
        elif ch == ord(" "):
            paused = not paused
        elif ch == ord("f"):
            process_one_frame = True
        elif ch == ord("s"):
            for i in range(100):
                ret, image = camera.read()
                frame_number += 1
            cv2.imshow('img', image)
        elif ch == ord("w"):
            for i in range(1000):
                ret, image = camera.read()
                frame_number += 1
            cv2.imshow('img', image)

    # FPS calc
    total_time = time.time() - start_time
    print("FPS: " + str(processed_frames / total_time))
