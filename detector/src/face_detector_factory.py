import os
import yaml


class FaceDetectorFactory:

    TENSORFLOW_MTCNN = 'tensorflow_mtcnn'
    TENSORFLOW_FACEBOXES = 'tensorflow_faceboxes'
    PADDLE_MTCNN = 'paddle_mtcnn'
    DLIB = 'dlib_mmod'

    @staticmethod
    def build(configuration):
        face_detector_type = configuration['type']

        if face_detector_type == FaceDetectorFactory.TENSORFLOW_MTCNN:
            from .face_detector_tensorflow_mtcnn import FaceDetectorTensorflowMTCNN
            return FaceDetectorTensorflowMTCNN()

        elif face_detector_type == FaceDetectorFactory.TENSORFLOW_FACEBOXES:
            from .face_detector_tensorflow_faceboxes import FaceDetectorTensorflowFaceboxes
            return FaceDetectorTensorflowFaceboxes()

        elif face_detector_type == FaceDetectorFactory.PADDLE_MTCNN:
            from .face_detector_paddle_mtcnn import FaceDetectorPaddleMTCNN
            return FaceDetectorPaddleMTCNN()

        elif face_detector_type == FaceDetectorFactory.DLIB:
            from .face_detector_dlib import FaceDetectorDlib
            return FaceDetectorDlib()

        else:
            raise SystemExit('ERROR: Invalid face detector type: ' + face_detector_type)

    @staticmethod
    def build_by_type(face_detector_type):
        try:
            config_path = os.path.dirname(os.path.realpath(__file__)) + "/../config/config_" + face_detector_type + ".yaml"
            return FaceDetectorFactory.build(FaceDetectorFactory._read_config_file(config_path))
        except FileNotFoundError:
            raise SystemExit('ERROR: Invalid face detector type: ' + face_detector_type)

    @staticmethod
    def _read_config_file(path):
        with open(path) as config_file:
            configuration = yaml.load(config_file, yaml.Loader)
            return configuration['face_detector']
