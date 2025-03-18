# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File handler

import os
from app.global_tools import Tools
from app.processing.frame_display import FrameDisplayer
from app.processing.image_captioning_handler import ImageCaptioningHandler
from app.processing.key_framing import KeyFraming


class FileHandler:
    def __init__(self, file_path, preview_element, progress_bar):
        self.file_path = file_path
        self.frame_displayer = FrameDisplayer(preview_element)
        self.progress_bar = progress_bar
        self.output_dir = "key_frames"

        # Delete old frames
        Tools.clear_frame_directories()

    # Extract keyframes from video
    def extract_keyframes(self):
        # Create instance of KeyFraming
        key_fr = KeyFraming(
            file_path=self.file_path, output_dir=self.output_dir, frames_to_retrieve=10
        )
        key_fr.extract_keyframes()

        # Generate captions for keyframes
        self.generate_captions()

    def generate_captions(self):
        # Create instance of ImageCaptioningHandler
        frame_caption_generator = ImageCaptioningHandler(
            original_output_dir=self.output_dir
        )

        # Get list of frames sorted alphabetically, and get total frames
        frames_path_list = sorted(os.listdir(self.output_dir))
        total_frames = len(frames_path_list)

        # Loop through frames and detect objects
        frame_count = 1
        for frame in frames_path_list:
            print(f"Processing frame {frame_count} of {total_frames}")

            # Caption frame
            generator_output = frame_caption_generator.frame_caption(frame)
            print("Generated caption: " + generator_output[1])

            # Display frame in preview window
            self.frame_displayer.display_frame(generator_output[0])

            # Update progress bar (second half of bar)
            self.progress_bar.setValue(50 + int((frame_count / total_frames) * 50))
            frame_count += 1
