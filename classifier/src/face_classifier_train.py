from classifier import FaceClassifierFactory
import sys
import numpy as np
import os
from utils.application.src.configuration import load_configuration

# This script trains a face classifier from a specified embeddings file, and saves
# the resulting classifier object using pickle

# Run this script from argus-system/
# Configure by changing ./face_classifier_train.yml

if __name__ == '__main__':

    base_dir = os.path.dirname(os.path.realpath(__file__))
    configuration = load_configuration(base_dir + '/face_classifier_train.yml')

    seed = 666
    np.random.seed(seed=seed)

    face_classifier_type = configuration['face_classifier_type']
    embeddings_file = configuration['embeddings_file']
    pickle_file = configuration['pickle_file']

    FaceClassifierFactory.train(face_classifier_type, embeddings_file, pickle_file)
