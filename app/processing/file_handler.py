# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File handler

import cv2
import os
from app.global_tools import Tools
from app.processing.frame_display import FrameDisplayer
from app.processing.image_captioning_handler import ImageCaptioningHandler


class FileHandler:
    def __init__(self, file_path, preview_element, progress_bar):
        self.file_path = file_path
        self.frame_displayer = FrameDisplayer(preview_element)
        self.progress_bar = progress_bar
        self.original_output_dir = "key_frames/original"
        self.total_frames = 0

        # Delete old frames
        Tools.clear_frame_directories()

    # Method to split video into frames
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
            frame_path = os.path.join(self.original_output_dir, f"{count:04d}.jpg")
            cv2.imwrite(frame_path, image)
            success, image = video_cap.read()
            print(f"Saving frame '{frame_path}'")

            # Display frame in preview window
            self.frame_displayer.display_frame(frame_path)

            count += 1

            # Update progress bar (first half of bar)
            self.progress_bar.setValue(int((count / self.total_frames) * 50))

        video_cap.release()

        # Detect objects in frames
        self.detect_objects()

    def detect_objects(self):
        # Create instance of ObjectDetectionHandler
        frame_caption_generator = ImageCaptioningHandler(
            original_output_dir=self.original_output_dir
        )

        # Order frames by number
        frames_path_list = sorted(
            os.listdir(self.original_output_dir), key=lambda x: int(x.split(".")[0])
        )

        # Loop through frames and detect objects
        frame_count = 1
        for frame in frames_path_list:
            print(f"Processing frame {frame_count} of {self.total_frames}")

            # Caption frame
            detector_output = frame_caption_generator.frame_caption(frame)
            print("Generated caption: " + detector_output[1])

            # Display frame in preview window
            self.frame_displayer.display_frame(detector_output[0])

            # Update progress bar (second half of bar)
            self.progress_bar.setValue(50 + int((frame_count / self.total_frames) * 50))
            frame_count += 1
