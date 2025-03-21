# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Key framing class
import os
import cv2
import matplotlib.pyplot as plt

# NOTES FOR REPORT: Mention here we started with katna but it didnt do what I wanted

class KeyFraming:
    def __init__(self, file_path, output_dir, frame_displayer):
        self.file_path = file_path
        self.output_dir = output_dir
        self.frame_displayer = frame_displayer

        # Split video method
        self.total_frames = 0
        self.all_frames = f"data/original_frames"

    # S Ghatak paper - Module 1
    def split_video(self):
        # Open video file
        video_cap = cv2.VideoCapture(self.file_path)
        if not video_cap.isOpened():
            print(f"Error: Could not open video file {self.file_path}")
            return

        success, image = video_cap.read()
        if not success:
            print("Error: Could not read video")
            video_cap.release()
            return

        self.total_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        count = 0

        while success:
            # Save frame as JPEG file
            frame_path = os.path.join(self.all_frames, f"{count:04d}.jpg")
            cv2.imwrite(frame_path, image)
            success, image = video_cap.read()
            print(f"Saving frame '{frame_path}'")

            # Display frame
            self.frame_displayer.display_frame(frame_path)

            count += 1

        video_cap.release()

    # S Ghatak paper - Module 2
    def calculate_frame_difference(self):
        # Read all frames from the directory
        frames = sorted(os.listdir(self.all_frames))
        frame_diffs = []

        for i in range(len(frames) - 1):
            print(f"Calculating frame difference for frame {frames[i]} and frame {frames[i + 1]}...")
            # Retrive frames
            frame_1_path = os.path.join(self.all_frames, frames[i])
            frame_2_path = os.path.join(self.all_frames, frames[i + 1])

            # Read two consecutive frames
            frame_1 = cv2.imread(frame_1_path)
            frame_2 = cv2.imread(frame_2_path)

            # Convert frames to grayscale
            frame_1_gray = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
            frame_2_gray = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)

            # Generate histograms
            self.generate_histograms(frame_1_gray, frame_2_gray, frame_1_path, frame_2_path)

        return frame_diffs

    # S Ghatak paper - Module 2 - Plot and save histograms
    def generate_histograms(self, frame_1_gray, frame_2_gray, frame_1_path, frame_2_path):
        # Calculate histograms (and flatten them)
        hist_1 = cv2.calcHist([frame_1_gray], [0], None, [256], [0, 256]).flatten()
        hist_2 = cv2.calcHist([frame_2_gray], [0], None, [256], [0, 256]).flatten()

        # Create figure for plotting (so it fits nicely in the window - 16:9/1080p)
        plt.figure(figsize=(19.2, 10.8), dpi=100)

        # Plot frame 1 and its histogram
        plt.subplot(2, 2, 1)
        plt.imshow(frame_1_gray, cmap='gray')
        plt.title("Frame 1 (Grayscale)")
        plt.axis('off')

        plt.subplot(2, 2, 3)
        plt.bar(range(256), hist_1, color='blue', alpha=0.7)
        plt.title("Histogram")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")

        # Plot frame 2 and its histogram
        plt.subplot(2, 2, 2)
        plt.imshow(frame_2_gray, cmap='gray')
        plt.title("Frame 2 (Grayscale)")
        plt.axis('off')

        plt.subplot(2, 2, 4)
        plt.bar(range(256), hist_2, color='red', alpha=0.7)
        plt.title("Histogram")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")

        plt.tight_layout()

        # Generate filename based on the frame paths
        frame1_num = os.path.basename(frame_1_path).split('.')[0]
        frame2_num = os.path.basename(frame_2_path).split('.')[0]
        hist_output_path = os.path.join("data/frame_histograms", f"hist_{frame1_num}_{frame2_num}.jpg")

        # Save figure and close
        plt.savefig(hist_output_path, dpi=100)
        plt.close()

        # Display histograms in preview window
        self.frame_displayer.display_frame(hist_output_path)

    # S Ghatak paper - All steps
    def extract_keyframes(self):
        print("Extracting keyframes...")
        # Module 1 - Extract frames
        self.split_video()

        # Module 2 - Calculate frame differences
        self.calculate_frame_difference()

        # Module 3 - Extract keyframes


        exit() # TEMP
