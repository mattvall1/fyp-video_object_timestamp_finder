# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script to retrive conceptual captions data
# Note: Download Conceptual Captions validation dataset from https://ai.google.com/research/ConceptualCaptions/download
import csv


def get_conceptual_captions():
    cc_lines = []
    print("Reading Conceptual Captions validation dataset...")
    with open("datasets/conceptual_captions/CC_Validate.tsv", "r") as f:
        read_file = csv.reader(f, delimiter="\t")
        count = 0
        for row in read_file:
            cc_lines.append(row)
            count += 1
    print(f"Read: {count}")

    return cc_lines

class ConceptualCaptions:
    def __init__(self):
        self.conceptual_captions = get_conceptual_captions()
        # Get all reference image URLs
        self.reference_image_urls = [image[1] for image in self.conceptual_captions]
        # Get all reference captions
        self.reference_captions = [caption[0] for caption in self.conceptual_captions]

    def get_conceptual_captions(self):
        return self.conceptual_captions

    def get_reference_image_urls(self):
        return self.reference_image_urls

    def get_reference_captions(self):
        return self.reference_captions
