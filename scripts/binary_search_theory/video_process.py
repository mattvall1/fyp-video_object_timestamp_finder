# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Get frames of a video and save them as JPEG files for testing
# Imports
import os
import cv2

def save_frames(video_path):
    video_cap = cv2.VideoCapture(video_path)

    success, image = video_cap.read()

    count = 0
    while success:
        # Save each frame as JPEG file
        frame_path = os.path.join('frames', f"{count:04d}.jpg")
        cv2.imwrite(frame_path, image)
        print(f"Saving frame '{frame_path}'")

        success, image = video_cap.read()
        count += 1

    video_cap.release()

if __name__ == "__main__":
    # Clear frames directory
    for file in os.listdir('frames'):
        os.remove(os.path.join('frames', file))

    # Save frames from video and search
    save_frames("../../testing_videos/highway_driving_2s.mp4")

