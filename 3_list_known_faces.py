import argparse
import os
import face_recognition
import concurrent.futures
import time
import json
import numpy as np
import datetime

# Adjust the threshold based on your requirement
certainty_threshold = 0.50
json_filename = "faces.json"

# Flag defaults
List_failed_matches = False
Delete_failed_matches = False
load_from_json = False
Output_report_to_file = False



# getting faces from json file
def load_known_faces_from_json(json_filename):
    with open(json_filename, 'r') as json_file:
        known_faces = json.load(json_file)
    return known_faces

# Create a class for encoding to json
class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyArrayEncoder, self).default(obj)



def encode_face(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    if not face_encodings:
        return None  # No faces found in the image
    return face_encodings[0]


def load_known_faces(known_faces_folder):
    known_faces = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {}
        for person_name in os.listdir(known_faces_folder):
            person_folder = os.path.join(known_faces_folder, person_name)
            if os.path.isdir(person_folder):
                #print(person_folder)
                image_files = [os.path.join(person_folder, image_file) for image_file in os.listdir(person_folder)]
                future_to_image = {executor.submit(encode_face, image_path): image_path for image_path in image_files}
                futures.update(future_to_image)

        for future in concurrent.futures.as_completed(futures):
            image_path = futures[future]
            person_name = os.path.basename(os.path.dirname(image_path))
            face_encoding = future.result()
            if face_encoding is not None:
                known_faces.setdefault(person_name, []).append(face_encoding)


    return known_faces



def process_image(image_path, known_faces, verbose):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        return (image_path, None)


    for person_name, known_encodings in known_faces.items():
        for face_encoding in face_encodings:
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            min_distance = min(face_distances)
            if min_distance < certainty_threshold:
                return (image_path, (person_name, min_distance))

    return (image_path, None)

def compare_faces_with_known_faces(face_folder, known_faces, verbose=False):
    matched_faces = {}
    unmatched_faces = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        image_files = []
        for root, _, files in os.walk(face_folder):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_files.append(os.path.join(root, file))

        futures = {executor.submit(process_image, image_path, known_faces, verbose): image_path for image_path in image_files}

        for future in concurrent.futures.as_completed(futures):
            image_path = futures[future]
            result = future.result()

            if result[1] is not None:
                person_name, min_distance = result[1]
                matched_faces.setdefault(person_name, []).append((os.path.basename(image_path), min_distance))
            else:
                unmatched_faces[os.path.basename(image_path)] = None
                if Delete_failed_matches:
                    os.remove(image_path) #remove unmatched

    return matched_faces, unmatched_faces



# Define a function to save the report to a file
def save_report_to_file(matched_faces, unmatched_faces, start_time):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"report-{current_datetime}.txt"

    with open(report_filename, 'w') as report_file:
        report_file.write("Matched faces:\n")
        for person_name, matched_files in sorted(matched_faces.items()):
            report_file.write(f"  {person_name}:\n")
            for file in matched_files:
                report_file.write(f"    {file}\n")

        if List_failed_matches:
            report_file.write("Unmatched faces:\n")
            for file in unmatched_faces:
                report_file.write(f"  {file}\n")

        end_time = time.time()
        duration = end_time - start_time
        report_file.write(f"Processing completed in {duration:.2f} seconds.\n")




def main():
    start_time =time.time()

    global certainty_threshold, List_failed_matches, Delete_failed_matches, load_from_json, Output_report_to_file

    parser = argparse.ArgumentParser(description="List known faces and process images.")
    parser.add_argument("-k","--known_faces_folder", default="./known_faces", help="Folder containing known faces images")
    parser.add_argument("-c", "--certainty_threshold", type=float, default=0.50, help="Threshold for face recognition certainty")
    parser.add_argument("-f", "--face_folder", default="./faces", help="Folder containing images to process")
    parser.add_argument("-j", "--load_from_json", action="store_true", help="Load known faces from a JSON file")
    parser.add_argument("-l", "--List_failed_matches", action="store_true", help="List images with no matched faces")
    parser.add_argument("-d", "--Delete_failed_matches", action="store_true", help="Delete images with no matched faces")
    parser.add_argument("-r", "--Output_report_to_file", action="store_true", help="Output report to a file")
   

    args = parser.parse_args()

    certainty_threshold = args.certainty_threshold
    List_failed_matches = args.List_failed_matches
    Delete_failed_matches = args.Delete_failed_matches
    load_from_json = args.load_from_json
    Output_report_to_file = args.Output_report_to_file

    known_faces_folder = args.known_faces_folder
    face_folder = args.face_folder

    if not os.path.exists(face_folder):
        os.makedirs(face_folder)



    if load_from_json:
        known_faces = load_known_faces_from_json(json_filename)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Known faces completed in {duration:.2f} seconds.")
    else:
        known_faces = load_known_faces(known_faces_folder)
            # Save known_faces to JSON
        with open(json_filename, 'w') as json_file:
            json.dump(known_faces, json_file, cls=NumpyArrayEncoder)



    matched_faces, unmatched_faces = compare_faces_with_known_faces(face_folder, known_faces)



    if not Output_report_to_file:

        # Output the report
        print("Matched faces:")
        for person_name, matched_files in sorted(matched_faces.items()):
            print(f"  {person_name}:")
            for file in matched_files:
                print(f"    {file}")

        if List_failed_matches :
            print("Unmatched faces:")
            for file in unmatched_faces:
                print(f"  {file}")

        end_time = time.time()
        duration = end_time - start_time
        print(f"Processing completed in {duration:.2f} seconds.")
    else :
        # Call the function to save the report to a file
        save_report_to_file(matched_faces, unmatched_faces, start_time)

if __name__ == "__main__":
    main()
