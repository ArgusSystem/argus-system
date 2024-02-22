import pickle
import numpy as np
from sklearn.svm import SVC


class SVClassifier:

    def __init__(self):
        self.model = SVC(kernel='linear', probability=True)
        self.class_names = None

    def train(self, embeddings_file_path):
        class_names, train_image_array, labels_train = load_images(embeddings_file_path)
        self.class_names = class_names
        self.model.fit(train_image_array, labels_train)

    def save(self, output_filename="svclassifier_edu_gabo.pkl"):
        with open(output_filename, "wb") as f:
            pickle.dump(self, f)

    def predict(self, embedding):
        predictions = self.model.predict_proba([embedding])
        best_class_index = np.argmax(predictions, axis=1)[0]
        best_class_probability = predictions[np.arange(1), best_class_index][0]

        return best_class_index, best_class_probability
    
    def contains(self, name):
        return name in self.class_names

    def get_name(self, class_index):
        return self.class_names[class_index]


def load_images(embeddings_file):

    # Load all images
    classes = {}
    class_names = []
    nrof_images = 0
    with open(embeddings_file, 'r') as f:
        for line in f:
            tokens = line.split(",")
            filename = tokens[0]
            filename_no_ext = filename.split(".")[0]
            class_name = " ".join(filename_no_ext.split("_")[:-1])

            embedding = np.array([float(e) for e in tokens[1:]])
            if class_name not in classes:
                classes[class_name] = {}
                class_names.append(class_name)

            classes[class_name][filename_no_ext] = embedding
            nrof_images += 1
    embedding_size = len(list(list(classes.values())[0].values())[0])

    images_array = np.zeros((nrof_images, embedding_size))
    images_array_index = 0
    labels = []

    for i in range(len(class_names)):
        class_name = class_names[i]

        images = list(classes[class_name].keys())
        np.random.shuffle(images)

        for image in images:
            images_array[images_array_index, :] = classes[class_name][image]
            images_array_index = images_array_index + 1
        labels += [class_name] * len(images)

    return class_names, images_array, labels
