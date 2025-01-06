# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File handler
from itertools import count

import cv2
import os
from app.global_tools import Tools
from app.processing.frame_display import FrameDisplayer


class ImageHandler:

    def __init__(self, file_path, preview_element, frame_details):
        self.file_path = file_path
        self.preview_element = preview_element
        self.frame_details = frame_details
        self.output_dir = 'key_frames'

        # Delete old frames
        Tools.clear_key_frames()


    # Method to split video into frames
    def split_video(self):
        # Open video file
        video_cap = cv2.VideoCapture(self.file_path)
        success, image = video_cap.read()
        count = 0

        while success:
            # Save frame as JPEG file
            frame_path = os.path.join(self.output_dir, f"{count:04d}.jpg")
            cv2.imwrite(frame_path, image)
            success, image = video_cap.read()
            print(f"Saving frame '{frame_path}'")
            self.frame_details.setText(f"Saving frame '{frame_path}'")
            count += 1

        video_cap.release()

        # Display frames
        self.display_frames()

    def display_frames(self):
        # Get list of frame files
        frame_files = os.listdir(self.output_dir)
        frame_files.sort()

        # Display frames
        frame_displayer = FrameDisplayer(self.preview_element, self.frame_details, self.output_dir)
        frame_displayer.display_frames()


