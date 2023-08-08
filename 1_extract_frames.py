import argparse
import subprocess
import time
import os
import multiprocessing

def get_num_cores():
    # Get the number of available cores on the system
    num_cores = multiprocessing.cpu_count()
    return min(num_cores, 6)  # Use up to 6 cores if available

def extract_frames(video_file, fps=1, duration=120, output_folder="images"):
    start_time = time.time()  # Record the start time

    num_cores = get_num_cores()

    # Construct the ffmpeg command
    command = f"ffmpeg -i \"{video_file}\" -r {fps} -ss 00:00:30 -t 00:02:30 -threads {num_cores} \"{output_folder}/{os.path.splitext(os.path.basename(video_file))[0]}_%04d.png\""

    # Execute the ffmpeg command
    subprocess.run(command, shell=True)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")

def process_folder(folder, fps=1, duration=120, output_folder="images"):
    if not os.path.exists(folder):
        print(f"Folder '{folder}' not found.")
        return

    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mkv')):
                video_file = os.path.join(root, file)
                extract_frames(video_file, fps, duration, output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from video files or folders.")
    parser.add_argument("input", help="Path to the input video file or folder")
    parser.add_argument("-f", "--fps", type=int, default=1, help="Frames per second (default: 1)")
    parser.add_argument("-t", "--duration", type=int, default=120, help="Duration in seconds (default: 120)")
    parser.add_argument("-o", "--output", default="images", help="Output folder (default: 'images')")
    args = parser.parse_args()

    if os.path.isfile(args.input):
        # Single video file provided
        extract_frames(args.input, args.fps, args.duration, args.output)
    elif os.path.isdir(args.input):
        # Folder provided, process all video files inside the folder
        process_folder(args.input, args.fps, args.duration, args.output)
    else:
        print("Invalid input. Please provide a valid video file or folder.")
        parser.print_help()
