# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Get detailed captions from images using BLIP model
# Imports
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText
from prettytable import PrettyTable
import os


class FrameSearcher:
    def __init__(self):
        self.device = "mps"
        # Load the BLIP model
        self.processor = AutoProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.model = AutoModelForImageTextToText.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        ).to(self.device)

    # Load and return image object
    def get_image(self, image_path):
        return Image.open(image_path)

    # Get caption for an image using BLIP
    def get_caption(self, image):
        inputs = self.processor(images=image, text=[""], return_tensors="pt").to(
            self.device
        )

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=50)
            caption = self.processor.decode(outputs[0], skip_special_tokens=True)
            return caption

    # Print caption
    def print_caption(self, caption):
        print(f"Caption: {caption}")

    # Find search term in the frame
    def find_in_frame(self, caption, search_term):
        if search_term.lower() in caption.lower():
            print(f"Found '{search_term}' in the frame.")
            return True
        else:
            print(f"'{search_term}' not found in the frame.")
            return False

    # Pipeline: load image, get caption, optionally show caption, and search
    def search_image(self, image_path, search_term, show_caption=True):
        image = self.get_image(image_path)
        caption = self.get_caption(image)
        if show_caption:
            self.print_caption(caption)
        return self.find_in_frame(caption, search_term)


# Main
if __name__ == "__main__":
    searcher = FrameSearcher()
    searcher.search_image("../../testing_images/trucks.jpg", "red truck")
