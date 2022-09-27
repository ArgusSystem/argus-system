#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from mtcnn import MTCNN
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


class FaceDetectorTensorflowMTCNN:
    def __init__(self):
        self.detector = MTCNN()

    def close(self):
        pass

    def detect_face_image(self, image):
        boxes = []
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        for detection in self.detector.detect_faces(img_rgb):
            # bboxes are in format [x, y, w, h]
            box = detection['box']
            # convert 3rd item to x+w
            box[2] = box[2] + box[0]
            # convert 4th item to y+h
            box[3] = box[3] + box[1]
            boxes.append(box)
        return boxes

    def detect_face(self, imgpath):
        img = cv2.imread(imgpath)
        return self.detect_face_image(img)
