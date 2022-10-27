import cv2
import numpy as np
import os
import paddle

# from .mobilefacenet_paddle.detection.face_detect import MTCNN

class FaceEmbedderPaddleMobilefacenet:

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # self.mtcnn = MTCNN(model_path=dir_path + "/mobilefacenet_paddle/models/mtcnn")

        self.required_size = (112, 112)
        self.model = paddle.jit.load(dir_path + "/mobilefacenet_paddle/models/infer/model")
        self.model.eval()

    def close(self):
        pass

    def process(self, imgs):
        imgs1 = []
        for img in imgs:
            img = cv2.resize(img, self.required_size)
            img = img.transpose((2, 0, 1))
            img = (img - 127.5) / 127.5
            imgs1.append(img)
        return imgs1

    def infer(self, img):
        assert len(img.shape) == 3 or len(img.shape) == 4
        if len(img.shape) == 3:
            img = img[np.newaxis, :]
        img = paddle.to_tensor(img, dtype='float32')
        feature = self.model(img)
        return feature.numpy()

    def get_embedding(self, image_path):
        # img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
        img = cv2.imread(os.path.expanduser(image_path))
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return self.get_embedding_mem(img)

    def get_embedding_mem(self, cv_image):
        #cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        # faces, boxes = self.mtcnn.infer_image(cv_image)
        # if faces is None:
        #     return [-1]
        faces = [cv_image]
        # cv2.imshow("face", faces[0])
        # cv2.waitKey(0)
        faces = self.process(faces)
        faces = np.array(faces, dtype='float32')
        features = self.infer(faces)
        return features[0]
