from .classifier_support_vector import SVClassifier
from .classifier_distance import DistanceClassifier
from .classifier_oneclass_svms import OneClassSVMClassifier
from .classifier_support_vector_with_oneclass import SVClassifierWithOneClass
import pickle
import os


class FaceClassifierFactory:

    SV_CLASSIFIER = 'sv_classifier'
    DISTANCE_CLASSIFIER = 'distance_classifier'
    ONECLASS_SVMS_CLASSIFIER = 'oneclass_svms_classifier'
    SV_CLASSIFIER_WITH_ONECLASS = 'sv_classifier_with_oneclass'

    @staticmethod
    def build(configuration):
        model_path = configuration['model']

        if configuration['minio'] == '':
            dir_path = os.path.dirname(os.path.realpath(__file__))
            model_path = dir_path + "/../../" + model_path

        with open(model_path, "rb") as f:
            return pickle.load(f, encoding="latin1")

    @staticmethod
    def train(face_classifier_type, embeddings_file, pickle_file):
        if face_classifier_type in classifier_classes.keys():
            # Train classifier
            classifier = classifier_classes[face_classifier_type]()
            classifier.train(embeddings_file)

            # Save trained classifier
            classifier.save(pickle_file)
        else:
            raise SystemExit('ERROR: Invalid face classifier type: ' + face_classifier_type)


classifier_classes = {
    FaceClassifierFactory.SV_CLASSIFIER: SVClassifier,
    FaceClassifierFactory.DISTANCE_CLASSIFIER: DistanceClassifier,
    FaceClassifierFactory.ONECLASS_SVMS_CLASSIFIER: OneClassSVMClassifier,
    FaceClassifierFactory.SV_CLASSIFIER_WITH_ONECLASS: SVClassifierWithOneClass
}