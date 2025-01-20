# Packages to install:
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
# pip install intel-openmp
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n-cls.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="imagenet-2012", epochs=100, imgsz=224, device=0, workers=0)

# Evaluate model performance on the validation set
metrics = model.val()

# Save the trained model
model.save("testing_1.pt")
