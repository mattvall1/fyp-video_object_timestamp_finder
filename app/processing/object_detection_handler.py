# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Image Captioning Handler
import shutil
from PyQt6 import QtCore


class ImageCaptioningHandler:
    def __init__(self, original_output_dir='key_frames'):
        self.original_output_dir = original_output_dir
        self.object_output_dir = 'key_frames/objects'
        pass

    def detect_objects(self, frame):
        frame_location = self.original_output_dir + "/" + frame
        # Detect objects in frame and save to output directory

        # ARTIFICIAL DETECTION WAIT
        QtCore.QThread.sleep(1)

        # Save detected objects to output directory
        shutil.copy(frame_location, self.object_output_dir) # Currently, just copy for prototyping

        # Return key words
        return [self.object_output_dir + "/" + frame, ["turtle", "rock", "stick"]]  # Example return value