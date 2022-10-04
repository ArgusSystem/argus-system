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
        self.face_embedder = InceptionResnetV1(pretrained='vggface2').eval()

    def close(self):
        pass

    def _preprocess_image(self, img):
        mean, std = img.mean(), img.std()
        # std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
        prewhitened = (img - mean) / std
        resized = cv2.resize(prewhitened, self.required_size)
        #final_image = np.expand_dims(resized, axis=0)
        return resized

    def get_embedding(self, image_path):
        img = cv2.imread(os.path.expanduser(image_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return self.get_embedding_mem(img)

    def get_embedding_mem(self, cv_image):
        face = self._preprocess_image(cv_image)
        transform = transforms.ToTensor()
        tensor = transform(face)
        embedding_tensor = self.face_embedder(tensor.float().unsqueeze(0))
        embedding = embedding_tensor.detach().numpy()[0]
        return embedding
