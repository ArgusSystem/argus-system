import pickle
import numpy as np

from scipy.special import softmax

MIN_SAMPLES_THRESHOLD = 10


class DistanceClassifier:

    def __init__(self):
        self.classes = []

    def train(self, embeddings_file_path):
        self.classes = load_images(embeddings_file_path)

    def save(self, output_filename="distanceclassifier_edu_gabo.pkl"):
        with open(output_filename, "wb") as f:
            pickle.dump(self, f)

    def predict(self, in_embedding):
        ids = []
        distances = []

        for i in range(len(self.classes)):
            for filename, file_embedding in self.classes[i][1]:
                d = np.sqrt(np.sum(np.square(in_embedding - file_embedding)))

                if d == 0:
                    return i, 1.0

                ids.append(i)
                distances.append(1/d)

        # Need a minimum number of samples to make sense out of the softmax function.
        # If number is too low, probabilities are very similar and tend to 1/N.
        if len(ids) < MIN_SAMPLES_THRESHOLD:
            return None, 0.0

        probabilities = softmax(np.array(distances))

        index = probabilities.argmax()

        return ids[index], probabilities[index]

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
