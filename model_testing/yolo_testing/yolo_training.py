# © 2024 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File to demonstrate how to train the YOLO model on a custom dataset.
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n-cls.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="imagenet100", epochs=5, imgsz=224, device="mps")

# Evaluate model performance on the validation set
metrics = model.val()

# Save the trained model
model.save("yolo_trained.pt")
