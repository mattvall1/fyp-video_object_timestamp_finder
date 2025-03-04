# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Image Captioning Handler
from ultralytics import YOLO


class ImageCaptioningHandler:
    def __init__(self, original_output_dir="key_frames"):
        self.original_output_dir = original_output_dir
        self.object_output_dir = "key_frames/objects/"
        self.model = YOLO(
            "processing/captioning_models/yolo_pretrained.pt"
        )  # Load pretrained model
        pass

    def _get_detected_captions(self, frame_location, frame):
        # Perform object detection on an image
        detection = self.model(frame_location)
        detection_output_filename = self.object_output_dir + f"{frame}.jpg"

        # Get possible objects to detect
        possible_objects = detection[0].names

        # Get a list of names of detected objects
        detected_objects = []
        for cls in detection[0].boxes.cls:
            detected_objects.append(possible_objects[cls.item()])

        # Save the image with the bounding boxes drawn on
        detection[0].save(detection_output_filename)

        # Return key words
        return [detected_objects, detection_output_filename]

    def detect_objects(self, frame):
        frame_location = self.original_output_dir + "/" + frame

        # Detect objects in frame and get detected object strings
        detector_output = self._get_detected_captions(frame_location, frame)

        # Return key words
        return [
            self.object_output_dir + "/" + frame,
            detector_output[0],
        ]  # Example return value
