import pickle
import numpy as np
from sklearn.svm import OneClassSVM
from .classifier_support_vector import load_images


class OneClassSVMClassifier:

    def __init__(self):
        self.models = {}  # Dictionary to store models for each class
        self.class_names = None

    def train(self, embeddings_file_path):
        class_names, train_image_array, labels_train = load_images(embeddings_file_path)
        self.class_names = class_names

        for class_name in class_names:
            # Create and train a separate OneClassSVM model for each class
            model = OneClassSVM()
            class_indices = [i for i, label in enumerate(labels_train) if label == class_name]
            class_embeddings = train_image_array[class_indices, :]
            model.fit(class_embeddings)
            self.models[class_name] = model

    def save(self, output_filename="svclassifier_edu_gabo.pkl"):
        with open(output_filename, "wb") as f:
            pickle.dump(self, f)

    def predict(self, embedding):
        class_scores = {}

        # Iterate over all models and predict scores
        for class_name, model in self.models.items():
            class_scores[class_name] = model.decision_function([embedding])[0]

        # Choose the class with the highest score
        best_class_name = max(class_scores, key=class_scores.get)
        best_class_score = class_scores[best_class_name]

        return self.class_names.index(best_class_name), best_class_score

    def contains(self, name):
        return name in self.class_names

    def get_name(self, class_index):
        return self.class_names[class_index]
