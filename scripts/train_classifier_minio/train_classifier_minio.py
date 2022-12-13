
import os
import yaml
from tempfile import gettempdir

from utils.image_processing.src.image_serialization import bytestring_to_image
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

with open(os.path.dirname(os.path.realpath(__file__)) + "/train_classifier_minio.yml") as config_file:
    configuration = yaml.safe_load(config_file)

EMBEDDINGS_FILE = configuration[EMBEDDINGS_FILE_KEY]
CLASSIFIER_FILE = configuration[CLASSIFIER_FILE_KEY]

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
people = Person.select(Person.id, Person.name, Person.photos, Person.created_at).order_by(Person.name).execute()

embedding_lines = []
for person in people:
    for photo in person.photos:
        # Get photo
        img_bytestring = people_storage.fetch(photo)

        # Perform face detection on photo
        img = bytestring_to_image(img_bytestring)
        bounding_boxes = face_detector.detect_face_image(img)
        x1, y1, x2, y2 = bounding_boxes[0]
        cropped_face = img[y1:y2, x1:x2]

        # Get embedding from face
        embedding = face_embedder.get_embedding_mem(cropped_face)

        # Add embedding to list
        emb_csv = ','.join(['%.8f' % num for num in embedding])
        line = photo + "," + emb_csv + "\n"
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
embeddings_filepath = os.path.join(LOCAL_DIR, EMBEDDINGS_FILE)
with open(embeddings_filepath, "w") as file:
    for line in embedding_lines:
        file.write(line)

# Store embeddings file
people_storage.store(name=EMBEDDINGS_FILE, filepath=embeddings_filepath)

# Train classifier with new embedding
try:
    classifier_filepath = os.path.join(LOCAL_DIR, CLASSIFIER_FILE)
    FaceClassifierFactory.train(face_classifier_type, embeddings_filepath, classifier_filepath)
    # Upload new trained model
    people_storage.store(name=CLASSIFIER_FILE, filepath=classifier_filepath)
# si hay solo 1 clase da error
except ValueError as e:
    print("ERROR: " + str(e) + " - Can't train classifier with less than two classes")
