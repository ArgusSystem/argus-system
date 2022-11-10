from classifier import FaceEmbedderFactory
import sys
import os
import cv2
import time
from shutil import copyfile
from utils.application.src.configuration import load_configuration

# This script gets all images in a directory (including subdirectories) and calculates each image's
# embedding using a specified face embedder type. Output is stored in .output/ and copied to the specified location.

# Run this script from argus-system/
# Configure by changing ./demo_embedding.yml

if __name__ == '__main__':

    base_dir = os.path.dirname(os.path.realpath(__file__))
    configuration = load_configuration(base_dir + '/demo_embedding.yml')

    # Create Face embedder
    face_embedder_type = configuration['face_embedder']
    face_embedder_object = FaceEmbedderFactory.build_by_type(face_embedder_type)

    output_folder_base = os.path.dirname(os.path.realpath(__file__)) + "/output"
    if not os.path.exists(output_folder_base):
        os.mkdir(output_folder_base)
    output_folder = output_folder_base + "/" + face_embedder_type
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # Get Face Embeddings
    image_paths_dir = configuration['images_dir']
    image_paths = []
    output_csv_filepath = output_folder_base + "/" + face_embedder_type + "/embeddings.txt"
    output_csv = open(output_csv_filepath, "w")
    for path, subdirs, files in os.walk(image_paths_dir):
        for name in files:
            image_paths.append(os.path.join(path, name))
    images = {}
    for i in range(len(image_paths)):
        image_path = image_paths[i]
        image = cv2.imread(image_path)
        images[image_path] = image

    print("Length: " + str(len(image_paths)))
    start_time = time.time()
    embeddings = {}
    for image_path in images:
        embeddings[image_path] = face_embedder_object.get_embedding_mem(images[image_path])
    elapsed_time = time.time() - start_time
    print("Total images: " + str(len(image_paths)) + ", Elapsed time: " + str(elapsed_time))

    for image_path in images:
        # Save embeddings to csv file in output folder
        emb = embeddings[image_path]
        filename = os.path.basename(image_path)
        emb_csv = ','.join(['%.8f' % num for num in emb])
        line = filename + "," + emb_csv + "\n"
        output_csv.write(line)
    output_csv.close()

    # Close face embedder
    face_embedder_object.close()

    output_embeddings_file = configuration['output_embeddings_file'] + "/embeddings_" + face_embedder_type + ".txt"
    copyfile(output_csv_filepath, output_embeddings_file)
