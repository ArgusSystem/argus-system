import cv2
import tensorflow as tf
import numpy as np
import sys
import os
import re
from .inception_resnet_v2 import InceptionResNetV2


class FaceEmbedderTensorflowFacenet:

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.required_size = (160, 160)
        self.face_embedder = InceptionResNetV2()
        self.face_embedder.load_weights(dir_path + "/../model/facenet_keras_weights.h5")

    def close(self):
        pass

    def _preprocess_image(self, img):
        mean, std = img.mean(), img.std()
        # std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
        prewhitened = (img - mean) / std
        resized = cv2.resize(prewhitened, self.required_size)
        final_image = np.expand_dims(resized, axis=0)
        return final_image

    def get_embedding(self, image_path):
        img = cv2.imread(os.path.expanduser(image_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return self.get_embedding_mem(img)

    def get_embedding_mem(self, cv_image):
        face = self._preprocess_image(cv_image)
        embedding_tensor = self.face_embedder(face, training=False)
        embedding = embedding_tensor.numpy()[0]
        return embedding
