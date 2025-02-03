# © 2024 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File to demonstrate how to train the YOLO model on a custom dataset.
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)

# Train the model (Windows/CUDA: device=0, workers=0 | macOS/Metal: device="mps")
results = model.train(data="coco8.yaml", epochs=100, imgsz=224, device=0, workers=0)

# Evaluate model performance on the validation set
metrics = model.val()

# Save the trained model
model.save("yolo_pretrained.pt")
