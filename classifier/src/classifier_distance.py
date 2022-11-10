import sys
import pickle
import numpy as np
import os


class DistanceClassifier:

    def __init__(self):
        self.classes = None

    def train(self, embeddings_file_path):
        self.classes = load_images(embeddings_file_path)

    def save(self, output_filename="distanceclassifier_edu_gabo.pkl"):
        with open(output_filename, "wb") as f:
            pickle.dump(self, f)

    def predict(self, in_embedding):

        min_id = -1
        min_dist = 999
        min_file = None
        for i in range(len(self.classes)):
            temp_name = self.classes[i][0]
            for filename, file_embedding in self.classes[i][1]:
                dist = np.sum(np.square(in_embedding - file_embedding))
                if dist < min_dist:
                    min_id = i
                    min_dist = dist
                    min_file = filename

        # min_dist = 1.24 -> prob = 0.7
        # min_dist = 0 -> prob = 1
        # min_dist = 4.14 -> prob = 0
        x_1 = 0
        x_0_7 = 0.8
        a = -0.3 / (x_0_7 + x_1)
        b = 1 - a * x_1

        prob = a * min_dist + b
        return min_id, prob
        #return min_id, min_dist

    def get_name(self, class_index):
        return self.classes[class_index][0]

    def contains(self, name):
        return name in [person[0] for person in self.classes]


def load_images(embeddings_file):

    # Load all images
    classes = {}
    with open(embeddings_file, 'r') as f:
        for line in f:
            tokens = line.split(",")
            filename = tokens[0]
            filename_no_ext = filename.split(".")[0]
            class_name = " ".join(filename_no_ext.split("_")[:-1])

            embedding = np.array([float(e) for e in tokens[1:]])
            if class_name not in classes:
                classes[class_name] = []

            classes[class_name].append([filename_no_ext, embedding])

    classes_list = []
    for name in classes.keys():
        classes_list.append([name, classes[name]])

    return classes_list
