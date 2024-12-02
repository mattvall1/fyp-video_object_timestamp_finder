from ultralytics import YOLO

# Load a model
model = YOLO("testing_1.pt")

# Perform object detection on an image
results = model("images/many_cats.jpg")
results[0].show()

# Export the model to ONNX format
path = model.export(format="onnx")  # return path to exported model