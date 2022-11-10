import sys
import os
import numpy as np
from classifier import FaceClassifierFactory
from utils.application.src.configuration import load_configuration
from classifier.src.classifier_distance import load_images

# This script takes an embeddings file and runs classification on each vector using a specified
# classifier object. It shows misclassified entries and outputs the total accuracy.
# the resulting classifier object using pickle

# Run this script from argus-system/
# Configure by changing ./classifier_accuracy.yml

if __name__ == '__main__':

    base_dir = os.path.dirname(os.path.realpath(__file__))
    configuration = load_configuration(base_dir + '/classifier_accuracy.yml')

    embeddings_file = configuration['embeddings_file']

    test_classes = load_images(embeddings_file)
    labels_test = []

    # Load classifier
    classifier = FaceClassifierFactory.build(configuration['face_classifier'])

    prob_t = configuration['probability_threshold']

    # Test classifier
    pred_equals = []
    for i in range(len(test_classes)):
        test_class_name = test_classes[i][0]
        for filename, file_embedding in test_classes[i][1]:
            pred_index, pred_prob = classifier.predict(file_embedding)
            pred_name = classifier.get_name(pred_index)
            known_person = classifier.contains(test_class_name)

            pred_correct = False
            if (known_person and classifier.get_name(pred_index) == test_class_name and pred_prob > prob_t) or \
                    (not known_person and pred_prob < prob_t):
                pred_correct = True

            if pred_correct:
                pred_equals.append(1)
            else:
                pred_equals.append(0)
                print('%4d  Real: %s, Predicted: %s, Prob: %.3f' % (i, test_class_name, classifier.get_name(pred_index), pred_prob))

    accuracy = np.mean(pred_equals)
    print('Accuracy: %.3f' % accuracy)
