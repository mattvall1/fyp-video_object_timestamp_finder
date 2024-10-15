from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device="mps")

# Evaluate model performance on the validation set
metrics = model.val()

# Save the trained model
model.save("testing_1.pt")
