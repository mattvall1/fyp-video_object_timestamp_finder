# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Standalone script to test azure API calls for image recognition.
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os


# Setup endpoint and client for Azure Vision
api_key = open("api_key.txt").read().strip()
endpoint = "https://fyp-msvision.cognitiveservices.azure.com/"
client = ComputerVisionClient(
    endpoint, credentials=CognitiveServicesCredentials(api_key)
)

# Get all image paths
image_paths = []
dir_paths = os.listdir("../../testing_images/small")
for dir_path in dir_paths:
    if dir_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")):
        image_paths.append("../../testing_images/small/" + dir_path)

# Analyse an image
for image_path in image_paths:
    features = ["Objects"]
    # Open image as binary stream (to send to Azure)
    with open(image_path, "rb") as image_stream:
        analysis = client.analyze_image_in_stream(image_stream, features)

    # Print all detected objects and their confidence scores
    print(f"\n--------------- {image_path} ---------------")
    for obj in analysis.objects:
        print(f"Object: {obj.object_property} (confidence: {obj.confidence:.2f})")
