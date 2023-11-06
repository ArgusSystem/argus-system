import cv2
import dlib

UPSCALE = 0


class FaceDetectorDlib:

    def __init__(self):
        self.detector = dlib.cnn_face_detection_model_v1('resources/mmod_human_face_detector.dat')

    def detect_face_image(self, image):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return [(rect.left(), rect.top(), rect.right(), rect.bottom())
                for rect in map(lambda x: x.rect, self.detector(img_rgb, UPSCALE))]

    def close(self):
        pass
