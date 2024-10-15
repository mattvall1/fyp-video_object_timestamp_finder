import os
import clip
import torch
import ssl
from PIL import Image
from torchvision.datasets import CIFAR100
from torchvision.datasets import ImageNet

# Used to override SSl issue (not secure)
ssl._create_default_https_context = ssl._create_unverified_context

# Load the model
device = "cpu"
model, preprocess = clip.load('ViT-B/32', device)
print("----------Model loaded----------")

# Download the dataset
# dataset = CIFAR100(root=os.path.expanduser("../../datasets/cifar-10"), download=True, train=False)
dataset = ImageNet(root=os.path.expanduser("../../datasets/imagenet-clip"))
print("----------Dataset loaded----------")

# Prepare the inputs
image = Image.open("images/orange_cat.jpeg")
image_input = preprocess(image).unsqueeze(0).to(device)
text_inputs = torch.cat([clip.tokenize(f"a photo of a {c}") for c in dataset.classes]).to(device)
print("----------Inputs prepared----------")

# Calculate features
with torch.no_grad():
    image_features = model.encode_image(image_input)
    text_features = model.encode_text(text_inputs)
print("----------Features calculated----------")

# Pick the top 5 most similar labels for the image
image_features /= image_features.norm(dim=-1, keepdim=True)
text_features /= text_features.norm(dim=-1, keepdim=True)
similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
values, indices = similarity[0].topk(5)
print("----------Top predictions calculated----------")

# Print the result
print("\nTop predictions:\n")
for value, index in zip(values, indices):
    print(f"{','.join(dataset.classes[index]):>16s}: {100 * value.item():.2f}%")