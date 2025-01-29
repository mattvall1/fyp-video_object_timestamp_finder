# © 2024 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File to demonstrate how to use the YOLO model to detect objects in an image (and print the results to the console).
from ultralytics import YOLO

# Load a model
model = YOLO("yolo_trained.pt")

# Perform object detection on an image
detection = model("../testing_images/many_cats.jpg")

# Get possible objects to detect
possible_objects = detection[0].names

# Get a list of names of detected objects
detected_objects = []
for cls in detection[0].boxes.cls:
    detected_objects.append(possible_objects[cls.item()])

# Print the detected objects
print(detected_objects)

# Save the image with the bounding boxes drawn on
detection[0].save("output.jpg")