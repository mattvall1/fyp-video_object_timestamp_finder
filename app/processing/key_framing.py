# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Key framing class
import shutil
from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter


class KeyFraming:
    def __init__(self, file_path, output_dir, frames_to_retrieve):
        self.file_path = file_path
        self.video = Video()
        self.output_dir = output_dir
        self.frames_to_retrieve = frames_to_retrieve

        # Initialize disk writer to save data at desired location
        self.disk_writer = KeyFrameDiskWriter(location=self.output_dir)

    def extract_keyframes(self):
        print("Extracting keyframes...")
        # Extract keyframes and process data
        self.video.extract_video_keyframes(
            no_of_frames=self.frames_to_retrieve,
            file_path=self.file_path,
            writer=self.disk_writer,
        )

        # Delete 'clipped' folder - we don't need it
        shutil.rmtree("clipped", ignore_errors=True)

        print("Keyframes extracted successfully.")
