# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Image Captioning Handler
import shutil
from ultralytics import YOLO
from PyQt6 import QtCore


class ImageCaptioningHandler:
    def __init__(self, original_output_dir='key_frames'):
        self.original_output_dir = original_output_dir
        self.object_output_dir = 'key_frames/objects'
        self.model = YOLO("captioning_models/yolo_pretrained.pt")  # Load pretrained model
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

    def get_detected_captions(self, frame):
        # Perform object detection on an image
        detection = self.model(frame)

        # Get possible objects to detect
        possible_objects = detection[0].names

        # Get a list of names of detected objects
        detected_objects = []
        for cls in detection[0].boxes.cls:
            detected_objects.append(possible_objects[cls.item()])

        # Return key words
        return [detected_objects, frame]  # Example return value
