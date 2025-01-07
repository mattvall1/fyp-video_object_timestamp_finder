# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Object Detection Handler
import shutil
from app.processing.frame_display import FrameDisplayer


class ObjectDetectionHandler:
    def __init__(self, original_output_dir='key_frames'):
        self.original_output_dir = original_output_dir
        self.object_output_dir = 'key_frames/objects'
        pass

    def detect_objects(self, frame):
        frame_location = self.original_output_dir + "/" + frame
        # Detect objects in frame and save to output directory

        # Save detected objects to output directory
        shutil.copy(frame_location, self.object_output_dir) # Currently, just copy for prototyping

        # Return key words
        return [self.object_output_dir + "/" + frame, ["person", "car", "dog"]]  # Example return value