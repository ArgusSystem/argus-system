from .classifier_support_vector import SVClassifier
from .classifier_distance import DistanceClassifier
import pickle
import os

classifier_classes = {
    'sv_classifier': SVClassifier,
    'distance_classifier': DistanceClassifier
}


class FaceClassifierFactory:

    @staticmethod
    def build(configuration):
        model_path = configuration['model']
        dir_path = os.path.dirname(os.path.realpath(__file__))
        full_save_path = dir_path + "/../../" + model_path
        with open(full_save_path, "rb") as f:
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
