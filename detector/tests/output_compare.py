import sys
import cv2
import os
from utils.image_processing.src.image_serialization import draw_boxes


def load_bboxes(bb_filename):
    bb_file = open(bb_filename, "r")
    bboxes = {}

    while True:
        image_name = bb_file.readline().strip()
        if not image_name:
            break
        bboxes[image_name] = []

        num_bboxes = int(bb_file.readline().strip())
        for j in range(num_bboxes):
            bbox = bb_file.readline().strip().split(",")
            bbox[2] = int(bbox[0]) + int(bbox[2])
            bbox[3] = int(bbox[1]) + int(bbox[3])
            bboxes[image_name].append(bbox)
    return bboxes


if __name__ == "__main__":

    if len(sys.argv) < 4:

        print("--------------------------------")
        print("This script receives files with validation bboxes and test bboxes and shows them in green and red respectively")
        print("")
        print("Usage: ")
        print("python output_compare.py 'bb_file_val' 'bb_file_test' 'image_path1' 'image_path2' ... ")
        print("--------------------------------")

    else:

        image_paths = sys.argv[3:]

        # Read bounding boxes from val file
        bb_filename_val = sys.argv[1]
        bboxes_val = load_bboxes(bb_filename_val)

        # Read bounding boxes from test file
        bb_filename_test = sys.argv[2]
        bboxes_test = load_bboxes(bb_filename_test)

        # Read and display images
        for i in range(len(image_paths)):

            # Read image
            image_path = image_paths[i]
            img = cv2.imread(image_path)

            # Draw bounding boxes
            image_name = os.path.basename(image_path)
            if image_name in bboxes_val:
                img = draw_boxes(img, bboxes_val[image_name], (0, 255, 0))
                pass
            if image_name in bboxes_test:
                img = draw_boxes(img, bboxes_test[image_name], (0, 0, 255))
                pass

            # Show image on screen
            cv2.imshow('img', img)
            ch = cv2.waitKey(0) & 0xFF
            if ch == ord("q"):
                break
