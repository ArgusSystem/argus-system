from classifier import FaceEmbedderFactory
import sys
import os

if __name__ == '__main__':

    if len(sys.argv) < 3:

        print("--------------------------------")
        print("This script receives a pretrained model and a list of prealigned images and calculates embeddings for each")
        print("")
        print("Usage: ")
        print("python demo_embedding.py ['tensorflow_facenet' | 'mvds_facenet'] 'image_path1' 'image_path2' ... ")
        print("--------------------------------")

    else:

        # Create Face embedder
        face_embedder_type = sys.argv[1]
        face_embedder_object = FaceEmbedderFactory.build_by_type(face_embedder_type)

        output_folder_base = os.path.dirname(os.path.realpath(__file__)) + "/output"
        if not os.path.exists(output_folder_base):
            os.mkdir(output_folder_base)
        output_folder = output_folder_base + "/" + face_embedder_type
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        # Get Face Embeddings
        image_paths = sys.argv[2:]
        output_csv = open(output_folder_base + "/" + face_embedder_type + "/embeddings.txt", "w")
        print("Length: " + str(len(image_paths)))
        for i in range(len(image_paths)):
            image_path = image_paths[i]
            emb = face_embedder_object.get_embedding(image_path)

            # Save embeddings to csv file in output folder
            filename = os.path.basename(image_path)
            emb_csv = ','.join(['%.8f' % num for num in emb])
            line = filename + "," + emb_csv + "\n"
            output_csv.write(line)
        output_csv.close()

        # Close face embedder
        face_embedder_object.close()
