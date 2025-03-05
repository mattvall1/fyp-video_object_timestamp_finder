# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script to retrieve TextCaps data
import json

def get_text_caps():
    text_caps = []
    print("Reading TextCaps validation dataset...")
    with open("../testing_data/text_caps/TextCaps_0.1_val.json", "r") as f:
        read_file = json.load(f)
        for row in read_file["data"]:
            text_caps.append(row)
    print(f"Read: {len(text_caps)}")

    return text_caps

class TextCaps:
    def __init__(self):
        self.text_caps = get_text_caps()
        # Get all reference image URLs
        self.reference_image_urls = [image["flickr_300k_url"] for image in self.text_caps]
        # Get all reference captions
        self.reference_captions = [caption["reference_strs"] for caption in self.text_caps]

    def get_text_caps(self):
        return self.text_caps

    def get_reference_image_urls(self):
        return self.reference_image_urls

    def get_reference_captions(self):
        return self.reference_captions
