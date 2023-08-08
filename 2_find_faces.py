import argparse
import os
import cv2
import face_recognition
import time
from concurrent.futures import ProcessPoolExecutor


def crop_face(input_image_path, output_image_path):
    # Load the image using face_recognition library
    image = face_recognition.load_image_file(input_image_path)

    # Find face locations in the image
    face_locations = face_recognition.face_locations(image)

    if not face_locations and list_no_face_found:
        print(f"No faces found in {input_image_path}")
        if Delete_processed_images:
            os.remove(input_image_path) #remove when done
        return

    # Process each face found in the image
    for i, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location

        # Crop the face region
        face_image = image[top:bottom, left:right]

        # Check if the cropped face is larger than 100x100 pixels
        if face_image.shape[0] >= 100 and face_image.shape[1] >= 100:
            # Save the cropped face to the output folder
            face_output_path = os.path.splitext(output_image_path)[0] + f'_f{i+1}.png'
            cv2.imwrite(face_output_path, cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR))
    os.remove(input_image_path) # remove image when done
            


def find_and_crop_faces(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    with ProcessPoolExecutor(max_workers=10) as executor:
        futures = []
        for image_file in image_files:
            input_image_path = os.path.join(input_folder, image_file)
            output_image_path = os.path.join(output_folder, image_file)

            future = executor.submit(crop_face, input_image_path, output_image_path)
            futures.append(future)
        
        # Wait for all threads to complete
        for future in futures:
            future.result()


def main():
    global list_no_face_found,Delete_processed_images
 
    # Create an ArgumentParser instance
    parser = argparse.ArgumentParser(description="Process images to find faces.")

    # Add arguments and flags to the parser
    parser.add_argument("input_folder", nargs="?", default="./images", help="Input folder for images")
    parser.add_argument("output_folder", nargs="?", default="./faces", help="Output folder for processed images")

    # Add optional flags
    parser.add_argument("-l", "--list_no_face_found", action="store_true", help="List images with no detected faces")
    parser.add_argument("-d", "--Delete_processed_images", action="store_true", help="Delete original images after processing")

    args = parser.parse_args()

    # Variables
    input_folder = args.input_folder
    output_folder = args.output_folder


    list_no_face_found = args.list_no_face_found
    Delete_processed_images = args.Delete_processed_images

    start_time = time.time()
    #Main method
    find_and_crop_faces(input_folder, output_folder)

    end_time = time.time()

    duration = end_time - start_time

    print(f"Processing completed in {duration:.2f} seconds.")


if __name__ == "__main__":
    main()
