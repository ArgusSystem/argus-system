import cv2
from .facenet_pytorch.inception_resnet_v1 import InceptionResnetV1
import numpy as np
import torchvision.transforms as transforms
import sys
import os
import re


class FaceEmbedderPytorchFacenet:

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.required_size = (160, 160)
        #self.face_embedder = InceptionResnetV1(pretrained='vggface2').eval()
        self.face_embedder = InceptionResnetV1(pretrained='casia-webface').eval()

    def close(self):
        pass

    def _preprocess_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # relative prewhitening
        mean, std = img.mean(), img.std()
        std_adj = std.clip(min=1.0 / (float(img.size) ** 0.5))
        #prewhitened = (img - mean) / std_adj
        # fixed prewhitening
        prewhitened = (img - 127.5) / 127.5
        # no prewhitening
        #prewhitened = img
        resized = cv2.resize(prewhitened, self.required_size)
        #cv2.imshow("prewhitened", prewhitened)
        #cv2.waitKey(1)
        return resized

    def get_embedding(self, image_path):
        img = cv2.imread(os.path.expanduser(image_path))
        return self.get_embedding_mem(img)

    def get_embedding_mem(self, cv_image):
        face = self._preprocess_image(cv_image)
        transform = transforms.ToTensor()
        tensor = transform(face)
        embedding_tensor = self.face_embedder(tensor.float().unsqueeze(0))
        embedding = embedding_tensor.detach().numpy()[0]
        return embedding
