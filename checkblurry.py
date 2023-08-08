import os
import cv2
import pandas as pd

def calculate_laplacian_variance(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray_image, cv2.CV_64F).var()
    return laplacian_var

def main():
    faces_folder = r'F:\summer23\facepi\faces'

    if not os.path.exists(faces_folder):
        print("Faces folder not found.")
        return

    # Create a list to store the results
    results = []

    # List all image files in the faces folder
    for root, _, files in os.walk(faces_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, file)
                face_image = cv2.imread(image_path)
                blur_score = calculate_laplacian_variance(face_image)
                results.append((os.path.basename(root), file, blur_score))

    # Convert the results list to a pandas DataFrame
    df = pd.DataFrame(results, columns=['Video', 'Face Image', 'Blur Score'])

    # Sort the DataFrame by 'Blur Score' column in descending order
    df_sorted = df.sort_values(by='Blur Score', ascending=False)

    # Output the top 10 images in tabular form
    top_10_images = df_sorted.head(10)
    print(top_10_images)

if __name__ == "__main__":
    main()
