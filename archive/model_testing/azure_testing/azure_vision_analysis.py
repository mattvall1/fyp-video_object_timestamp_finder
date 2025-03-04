# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Standalone script to test azure API calls for image analysis.
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

# Setup endpoint and client for Azure Vision
api_key = open("api_key.txt").read().strip()
endpoint = "https://fyp-msvision.cognitiveservices.azure.com/"

client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

# Get all image paths
image_paths = []
dir_paths = os.listdir("../../testing_images/small")
for dir_path in dir_paths:
    if dir_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")):
        image_paths.append("../../testing_images/small/" + dir_path)

# Select features
features = [VisualFeatures.DENSE_CAPTIONS, VisualFeatures.OBJECTS]

# Get byte stream of image and analyse
for image_path in image_paths:
    with open(image_path, "rb") as image_stream:
        image_data = image_stream.read()

    analysis = client.analyze(
        image_data=image_data, visual_features=features, language="en"
    )

    if analysis.dense_captions is not None:
        for caption in analysis.dense_captions.list:
            print(f"{caption.text} - Confidence: {caption.confidence:.4f}")
