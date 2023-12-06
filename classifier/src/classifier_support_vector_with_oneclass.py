import pickle
import numpy as np
from sklearn.svm import SVC, OneClassSVM
from .classifier_support_vector import load_images


class SVClassifierWithOneClass:

    def __init__(self):
        self.model = SVC(probability=True)
        self.one_class_model = OneClassSVM()
        self.class_names = None

    def train(self, embeddings_file_path):
        class_names, train_image_array, labels_train = load_images(embeddings_file_path)
        self.class_names = class_names

        # Train OneClassSVM on all images from all labels
        all_images_array = np.vstack(list(train_image_array))
        self.one_class_model.fit(all_images_array)

        # Train multiclass SVM
        self.model.fit(train_image_array, labels_train)

    def save(self, output_filename="svclassifier_edu_gabo.pkl"):
        with open(output_filename, "wb") as f:
            pickle.dump(self, f)

    def predict(self, embedding):
        # Use OneClassSVM to check if the embedding belongs to any known label
        if self.one_class_model.predict([embedding])[0] == -1:
            # Unknown label, return probability of 0
            return 0, 0.0

        # Predict using the multiclass SVM
        predictions = self.model.predict_proba([embedding])
        best_class_index = np.argmax(predictions, axis=1)[0]
        best_class_probability = predictions[np.arange(1), best_class_index][0]

        return best_class_index, best_class_probability

    def contains(self, name):
        return name in self.class_names

    def get_name(self, class_index):
        return self.class_names[class_index]
