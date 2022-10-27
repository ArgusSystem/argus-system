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
        bboxes = [[int(p) for p in bbox[:4]] for bbox in self.detector(image)]
        # if len(bboxes) > 0:
        #     pad = int(max(bboxes[0][2] - bboxes[0][0], bboxes[0][3] - bboxes[0][1]) * 0.1)
        #     bboxes = [[bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad] for bbox in bboxes]
        return bboxes

    def detect_face(self, imgpath):
        img = cv2.imread(imgpath)
        return self.detect_face_image(img)
