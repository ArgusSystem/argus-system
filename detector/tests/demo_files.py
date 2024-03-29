import sys
import cv2
import os
import time
import shutil
import yaml
from detector.src import FaceDetectorFactory
from utils.application.src.configuration import load_configuration

# This script gets all images in a directory (including subdirectories) and performs face detection
# on them using the specified detector.
# The output is stored in ./output/ as an embeddings.txt file and a directory of cropped faces.

# Run this script from argus-system/
# Configure by changing ./demo_files.yml


def drawBoxes(im, boxes):

    for i in range(boxesAmount(boxes)):
        box = boxes[i]
        x1 = box[0]
        y1 = box[1]
        x2 = box[2]
        y2 = box[3]
        cv2.rectangle(im, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
    return im

def boxesAmount(boxes):
    return len(boxes)

def boxesCSVLines(img_path, boxes):

    lines = img_path + "\n"
    bbAmount = boxesAmount(boxes)
    lines += str(bbAmount) + "\n"

    for i in range(bbAmount):
        box = boxes[i]
        x1 = box[0]
        y1 = box[1]
        x2 = box[2]
        y2 = box[3]
        lines += str(int(x1)) + " " + str(int(y1)) + " " + str(int(x2) - int(x1)) + " " + str(int(y2) - int(y1)) + " 0 0 0 0 0 0\n"
    return lines


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.realpath(__file__))
    configuration = load_configuration(base_dir + '/demo_files.yml')

    # Create Face Detector
    face_detector_type = configuration['face_detector']
    faceDetectorObject = FaceDetectorFactory.build_by_type(face_detector_type)

    # Get output folder
    output_folder_base = os.path.dirname(os.path.realpath(__file__)) + "/output"
    if not os.path.exists(output_folder_base):
        os.mkdir(output_folder_base)
    output_folder = output_folder_base + "/" + face_detector_type
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # Load Images
    image_paths_dir = configuration['images_dir']
    image_paths = []
    for path, subdirs, files in os.walk(image_paths_dir):
        for name in files:
            image_paths.append(os.path.join(path, name))
    images = {}
    for i in range(len(image_paths)):
        image_path = image_paths[i]
        image = cv2.imread(image_path)
        images[image_path] = image

    # Detect Bounding Boxes
    print("Length: " + str(len(image_paths)))
    start_time = time.time()
    total_boxes = []
    for image_path in images:
        # Detect face bounding boxes
        boundingboxes = faceDetectorObject.detect_face_image(images[image_path])
        total_boxes.append(boundingboxes)
    elapsed_time = time.time() - start_time
    print("Total images: " + str(len(image_paths)) + ", Elapsed time: " + str(elapsed_time))

    # Close Face Detector
    faceDetectorObject.close()

    # Save Bounding Boxes to file
    output_csv = open(output_folder + "/bounding_boxes.txt", "w")
    for i in range(len(image_paths)):
        image_path = image_paths[i]
        boundingboxes = total_boxes[i]

        # Show on screen
        #img = cv2.imread(image_path)
        #img = drawBoxes(img, boundingboxes)
        #cv2.imshow('img', img)
        #ch = cv2.waitKey(0) & 0xFF
        #if ch == ord("q"):
        #    break

        # Save bounding boxes to csv file in output folder
        #filename = os.path.basename(image_path)
        filename = image_path.replace(image_paths_dir, "")[1:]
        filename = filename.replace("\\", "/")
        #print(filename)
        line = boxesCSVLines(filename, boundingboxes)
        output_csv.write(line)
    output_csv.close()

    # Save cropped faces to folder
    faces_folder = output_folder + "/faces"
    if os.path.exists(faces_folder):
        shutil.rmtree(faces_folder)
    os.mkdir(faces_folder)
    for i in range(len(image_paths)):

        image_path = image_paths[i]
        img = cv2.imread(image_path)

        filename = faces_folder + "/" + os.path.basename(image_path)

        boundingboxes = total_boxes[i]
        for j in range(len(boundingboxes)):
            box = boundingboxes[j]
            x1 = int(box[0])
            y1 = int(box[1])
            x2 = int(box[2])
            y2 = int(box[3])

            face = img[y1:y2, x1:x2].copy()
            face_filename = filename
            if len(boundingboxes) > 1:
                filename_split = filename.split(".")
                face_filename = filename_split[0] + "-" + str(j) + "." + filename_split[1]
            cv2.imwrite(face_filename, face)
            # try:
            #     #face = cv2.resize(face, (160, 160), interpolation=cv2.INTER_CUBIC)
            # except:
            #     print("Bad box on:", image_path, ", box number:", i, ", box:", box)

