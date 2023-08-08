import os
import cv2
import face_recognition
import dlib
from pathlib import Path
import shutil

def estimate_face_pose(face_image):
    # Load the face pose estimation model
    pose_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Find facial landmarks
    face_landmarks = face_recognition.face_landmarks(face_image)
    if len(face_landmarks) == 0:
        return None

    # Use facial landmarks to estimate the face pose
    shape = face_recognition.face_locations(face_image)
    dlib_shape = dlib.rectangle(shape[0][3], shape[0][0], shape[0][1], shape[0][2])
    pose = pose_predictor(face_image, dlib_shape)
    return pose

def main():
    faces_folder = r'F:\summer23\facepi\faces'
    output_folder = r'F:\summer23\facepi\faces_front'

    if not os.path.exists(faces_folder):
        print("Faces folder not found.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create a list to store the results
    results = []

    # List all image files in the faces folder
    for root, _, files in os.walk(faces_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, file)
                face_image = cv2.imread(image_path)
                pose = estimate_face_pose(face_image)
                if pose is not None:
                    # Calculate a score for face pose (lower score means better alignment with the camera)
                    center_x = sum(p.x for p in pose.parts()) / len(pose.parts())
                    center_y = sum(p.y for p in pose.parts()) / len(pose.parts())
                    score = sum(abs(p.x - center_x) + abs(p.y - center_y) for p in pose.parts()) / len(pose.parts())
                    results.append((file, score))

    # Sort the images based on face pose score
    results.sort(key=lambda x: x[1])

    # Copy the top 20 images to the output folder
    for i, (file, _) in enumerate(results[:20]):
        src_path = os.path.join(faces_folder, file)
        dst_path = os.path.join(output_folder, file)
        shutil.copy(src_path, dst_path)

if __name__ == "__main__":
    main()
