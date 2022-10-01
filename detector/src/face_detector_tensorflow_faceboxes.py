#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os
from .faceboxes.core.api.face_detector import FaceDetector


class FaceDetectorTensorflowFaceboxes:
    def __init__(self):
        model_path = os.path.dirname(os.path.realpath(__file__)) + "/faceboxes/model"
        self.detector = FaceDetector(model_path)

    def close(self):
        pass

    def detect_face_image(self, image):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return self.detector(img_rgb)

    def detect_face(self, imgpath):
        img = cv2.imread(imgpath)
        return self.detect_face_image(img)
