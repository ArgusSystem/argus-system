#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from .mtcnn_paddle.face_detect import MTCNN


class FaceDetectorPaddleMTCNN:
    def __init__(self):
        self.detector = MTCNN()

    def close(self):
        pass

    def detect_face_image(self, image):
        boxes = []
        imgs, mtcnn_boxes = self.detector.infer_image(image)
        if mtcnn_boxes is not None:
            boxes = mtcnn_boxes[:4]
            #cv2.imshow("imgrot", imgs[0])
            #cv2.waitKey(1)
        return boxes

    def detect_face(self, imgpath):
        img = cv2.imread(imgpath)
        return self.detect_face_image(img)
