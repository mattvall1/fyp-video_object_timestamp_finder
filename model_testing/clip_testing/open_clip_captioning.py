# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File to demonstrate OpenCLIP model
import torch
from PIL import Image
import open_clip
import os

# Show available pretrained models
# print(open_clip.list_pretrained())

# Load the model
model, _, transform = open_clip.create_model_and_transforms(
    'coca_ViT-L-14', 
    pretrained='mscoco_finetuned_laion2b_s13b_b90k',
    device='cuda'
)

# Load the image
for image_path in os.listdir("testing_images"):
    image = Image.open(f"testing_images/{image_path}")
    image = transform(image).unsqueeze(0).to(torch.float32).to('cuda')

    # Get the features
    with torch.no_grad(), torch.amp.autocast('cuda'):
        generation = model.generate(image)

    # Print the features
    print(open_clip.decode(generation[0]).split("<end_of_text>")[0].replace("<start_of_text>", ""))
