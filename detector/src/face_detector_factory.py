import os
import yaml


class FaceDetectorFactory:

    @staticmethod
    def build(configuration):
        face_detector_type = configuration['type']

        if face_detector_type == "tensorflow_mtcnn":
            from .face_detector_tensorflow_mtcnn import FaceDetectorTensorflowMTCNN
            return FaceDetectorTensorflowMTCNN()

        elif face_detector_type == "caffe_mtcnn":
            from .face_detector_caffe_mtcnn import FaceDetectorCaffeMTCNN
            return FaceDetectorCaffeMTCNN()

        elif face_detector_type == "movidius_mtcnn":
            from .face_detector_movidius_mtcnn import FaceDetectorMovidiusMTCNN
            return FaceDetectorMovidiusMTCNN(configuration['movidius_id_pnet'], configuration['movidius_id_onet'])

        elif face_detector_type == "movidius_ssd":
            from .face_detector_movidius_ssd import FaceDetectorMovidiusSSD
            return FaceDetectorMovidiusSSD(configuration['movidius_id'], configuration['longrange'])
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
