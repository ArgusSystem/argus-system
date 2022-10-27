import os
import yaml


class FaceEmbedderFactory:

    @staticmethod
    def build(configuration):
        face_embedder_type = configuration['type']

        if face_embedder_type == "tensorflow_facenet":
            from .face_embedder_tensorflow_facenet import FaceEmbedderTensorflowFacenet
            return FaceEmbedderTensorflowFacenet()

        elif face_embedder_type == "pytorch_facenet":
            from .face_embedder_pytorch_facenet import FaceEmbedderPytorchFacenet
            return FaceEmbedderPytorchFacenet()

        elif face_embedder_type == "paddle_mobilefacenet":
            from .face_embedder_paddle_mobilefacenet import FaceEmbedderPaddleMobilefacenet
            return FaceEmbedderPaddleMobilefacenet()

        else:
            raise SystemExit('ERROR: Invalid face embedder type: ' + face_embedder_type)

    @staticmethod
    def build_by_type(face_embedder_type):
        try:
            config_path = os.path.dirname(os.path.realpath(__file__)) + "/../config/config_" + face_embedder_type + ".yaml"
            return FaceEmbedderFactory.build(FaceEmbedderFactory._read_config_file(config_path))
        except FileNotFoundError:
            raise SystemExit('ERROR: Invalid face embedder type: ' + face_embedder_type)

    @staticmethod
    def _read_config_file(path):
        with open(path) as config_file:
            configuration = yaml.load(config_file, yaml.Loader)
            return configuration['face_embedder']
