
import os
import yaml
import cv2
from tempfile import gettempdir

from utils.image_processing.src.image_serialization import bytestring_to_image, write_text_with_background, resize_keep_aspect_ratio
from utils.video_storage import StorageFactory, StorageType
from utils.orm.src.database import connect
from utils.orm.src import Person
from detector import FaceDetectorFactory
from classifier import FaceEmbedderFactory, FaceClassifierFactory
from minio.error import S3Error

LOCAL_DIR = gettempdir()
FACE_DETECTOR_KEY = 'face_detector'
FACE_EMBEDDER_KEY = 'face_embedder'
EMBEDDINGS_FILE_KEY = 'embeddings_file'
CLASSIFIER_FILE_KEY = 'classifier_file'
DB_KEY = 'db'
STORAGE_KEY = 'storage'
CLASSIFIER_TYPE_KEY = 'classifier_type'
USER_INTERACTION = 'user_interaction_on_multiple_faces'


def train_model():
    with open(os.path.dirname(os.path.realpath(__file__)) + "/train_classifier_minio.yml") as config_file:
        configuration = yaml.safe_load(config_file)

    embeddings_file = configuration[EMBEDDINGS_FILE_KEY]
    classifier_file = configuration[CLASSIFIER_FILE_KEY]
    ask_user_interaction = configuration[USER_INTERACTION]

    # Connect to db
    connect(**configuration[DB_KEY])

    # Setup people photos storage
    people_storage = StorageFactory(**configuration[STORAGE_KEY]).new(StorageType.PEOPLE)

    # Create face detector
    face_detector = FaceDetectorFactory.build(configuration[FACE_DETECTOR_KEY])

    # Create face embedder
    face_embedder = FaceEmbedderFactory.build(configuration[FACE_EMBEDDER_KEY])

    # Set classifier type
    face_classifier_type = configuration[CLASSIFIER_TYPE_KEY]

    # Get people list from db
    people = Person.select(Person.id, Person.name, Person.created_at).order_by(Person.id).execute()

    embedding_lines = []
    for person in people:
        for photo in person.photos():
            # Get photo
            img_bytestring = people_storage.fetch(photo.filename)
            img = bytestring_to_image(img_bytestring)
            cropped_face = img
            add_face = True

            if not photo.preprocessed:
                # Perform face detection on photo
                bounding_boxes = face_detector.detect_face_image(img)

                if len(bounding_boxes) <= 0:
                    continue

                # Get the first face
                x1, y1, x2, y2 = bounding_boxes[0]
                cropped_face = img[y1:y2, x1:x2]

                # If there are many faces in the photo, check which one to add to the model
                if ask_user_interaction and len(bounding_boxes) > 1:
                    for bounding_box in bounding_boxes:
                        x1, y1, x2, y2 = bounding_box
                        cropped_face = img[y1:y2, x1:x2]

                        # Show cropped face and ask for user confirmation to add it to model
                        cropped_face_copy = cropped_face.copy()
                        cropped_face_copy = resize_keep_aspect_ratio(cropped_face_copy, width=600)
                        cropped_face_copy = write_text_with_background(cropped_face_copy, person.name + ". Add to model y/n")
                        cv2.imshow("face", cropped_face_copy)

                        # Check user y/n
                        ch = ord(" ")
                        while ch != ord("y") and ch != ord("n"):
                            ch = cv2.waitKey(0) & 0xFF
                        add_face = ch == ord("y")

                        # If yes, skip all other faces in this photo
                        if add_face:
                            break

            if add_face:
                # Get embedding from face
                embedding = face_embedder.get_embedding_mem(cropped_face)

                # Add embedding to list
                emb_csv = ','.join(['%.8f' % num for num in embedding])
                line = photo.filename.replace(person.name, str(person.id)) + "," + emb_csv + "\n"
                embedding_lines.append(line)

                # # Get embeddings file
                # embeddings_filepath = path.join(LOCAL_DIR, EMBEDDINGS_FILE)
                # try:
                #     people_storage.fetch(EMBEDDINGS_FILE, embeddings_filepath)
                # except S3Error:
                #     with open(embeddings_filepath, 'w') as blank_file:
                #         pass
                #
                # # Add new embedding to embeddings file
                # with open(embeddings_filepath, "a") as file:
                #     emb_csv = ','.join(['%.8f' % num for num in embedding])
                #     line = new_photo_id + "," + emb_csv + "\n"
                #     file.write(line)
                #
                # # Store new embeddings file
                # people_storage.store(name=EMBEDDINGS_FILE, filepath=embeddings_filepath)

    # Write embeddings file
    embeddings_filepath = os.path.join(LOCAL_DIR, embeddings_file)
    with open(embeddings_filepath, "w") as file:
        for line in embedding_lines:
            file.write(line)

    # Store embeddings file
    people_storage.store(name=embeddings_file, filepath=embeddings_filepath)

    # Train classifier with new embedding
    try:
        classifier_filepath = os.path.join(LOCAL_DIR, classifier_file)
        FaceClassifierFactory.train(face_classifier_type, embeddings_filepath, classifier_filepath)
        # Upload new trained model
        people_storage.store(name=classifier_file, filepath=classifier_filepath)
    # si hay solo 1 clase da error
    except ValueError as e:
        print("ERROR: " + str(e) + " - Can't train classifier with less than two classes")


if __name__ == "__main__":
    train_model()
