import sys
import os
import numpy as np
from classifier import FaceClassifierFactory
from utils.application.src.configuration import load_configuration
from classifier.src.classifier_distance import load_images
import time


def calc_prob_minmax(prob, prob_minmax):
    min = prob if prob < prob_minmax[0] else prob_minmax[0]
    max = prob if prob > prob_minmax[1] else prob_minmax[1]
    return [min, max]


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

    start_time = time.time()
    total_faces = 0

    # Test classifier
    pred_match = []
    match_prob_minmax = [999, -999]
    pred_miss = []
    miss_prob_minmax = [999, -999]
    pred_thresh_miss = []
    thresh_miss_prob_minmax = [999, -999]
    pred_unknown_miss = []
    unknown_miss_prob_minmax = [999, -999]
    for i in range(len(test_classes)):
        test_class_name = test_classes[i][0]
        for filename, file_embedding in test_classes[i][1]:
            total_faces += 1

            pred_index, pred_prob = classifier.predict(file_embedding)
            pred_name = classifier.get_name(pred_index)
            known_person = classifier.contains(test_class_name)

            flag_match = False
            flag_miss = False
            flag_thresh_miss = False
            flag_unknown_miss = False

            if known_person:
                if classifier.get_name(pred_index) == test_class_name:
                    if pred_prob > prob_t:
                        flag_match = True
                        match_prob_minmax = calc_prob_minmax(pred_prob, match_prob_minmax)
                    else:
                        #print('THRESH MISS %4d %s Real: %s, Predicted: %s, Prob: %f' % (i, filename, test_class_name, classifier.get_name(pred_index), pred_prob))
                        flag_thresh_miss = True
                        thresh_miss_prob_minmax = calc_prob_minmax(pred_prob, thresh_miss_prob_minmax)
                else:
                    #print('MISS %4d %s Real: %s, Predicted: %s, Prob: %f' % (i, filename, test_class_name, classifier.get_name(pred_index), pred_prob))
                    flag_miss = True
                    miss_prob_minmax = calc_prob_minmax(pred_prob, miss_prob_minmax)
            else:
                if pred_prob < prob_t:
                    flag_match = True
                    match_prob_minmax = calc_prob_minmax(pred_prob, match_prob_minmax)
                else:
                    #print('UNKNOWN MISS %4d %s Real: %s, Predicted: %s, Prob: %f' % (i, filename, test_class_name, classifier.get_name(pred_index), pred_prob))
                    flag_unknown_miss = True
                    unknown_miss_prob_minmax = calc_prob_minmax(pred_prob, unknown_miss_prob_minmax)

            pred_match.append(int(flag_match))
            pred_miss.append(int(flag_miss))
            pred_thresh_miss.append(int(flag_thresh_miss))
            pred_unknown_miss.append(int(flag_unknown_miss))

    elapsed_time = time.time() - start_time
    print("Total images: " + str(total_faces) + ", Elapsed time: " + str(elapsed_time))

    print('Accuracy: %f' % np.mean(pred_match))
    print('Min: %f Max: %f' % tuple(match_prob_minmax))
    print()

    print('Miss predictions: %f' % np.mean(pred_miss))
    print('Min: %f Max: %f' % tuple(miss_prob_minmax))
    print()

    print('Threhold miss predictions: %f' % np.mean(pred_thresh_miss))
    print('Min: %f Max: %f' % tuple(thresh_miss_prob_minmax))
    print()

    print('Unknown miss predictions: %f' % np.mean(pred_unknown_miss))
    print('Min: %f Max: %f' % tuple(unknown_miss_prob_minmax))
    print()
