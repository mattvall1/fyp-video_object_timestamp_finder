# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File to demonstrate OpenCLIP model
import torch
from PIL import Image
import open_clip

# Show available pretrained models
open_clip.list_pretrained()

# Load the model
model, preprocess = open_clip.load('ViT-H-14-378-quickgelu')