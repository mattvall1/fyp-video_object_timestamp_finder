# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Find specific text in a a frame, after applying captioning algorithm on it
# Imports
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from prettytable import PrettyTable

class FrameSearcher:
    def __init__(self, endpoint="https://fyp-msvision.cognitiveservices.azure.com/", api_key_path='api_key.txt'):
        self.client = ImageAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(open(api_key_path).read().strip())
        )
        self.features = [VisualFeatures.DENSE_CAPTIONS, VisualFeatures.OBJECTS]

    # Read and return image bytes from file
    def get_image(self, image_path):
        with open(image_path, 'rb') as file:
            return file.read()

    # Analyze image and return captions with bounding boxes and confidence scores
    def get_captions(self, image):
        analysis = self.client.analyze(image_data=image, visual_features=self.features, language="en")

        image_captions = []
        if analysis.dense_captions is not None:
            for caption in analysis.dense_captions.list:
                image_captions.append([caption.text, caption.bounding_box, caption.confidence])

        return image_captions

    # Print captions in a table
    def print_captions_table(self, captions):
        table = PrettyTable()
        table.field_names = ['Caption', 'Bounding box', 'Confidence']
        for caption in captions:
            table.add_row(caption)
        print(table)

    # Find search term in the frame
    def find_in_frame(self, captions, search_term):
        matches = []
        for caption in captions:
            if search_term in caption[0]:
                matches.append(caption[1])

        if not matches:
            print(f"'{search_term}' not found in the frame.")
        else:
            for bbox in matches:
                print(f"Found '{search_term}' in bounding box: {bbox}")
        return matches

    # Pipeline: load image, get captions, optionally show table, and search
    def search_image(self, image_path, search_term, show_table=True):
        image = self.get_image(image_path)
        captions = self.get_captions(image)
        if show_table:
            self.print_captions_table(captions)
        return self.find_in_frame(captions, search_term)

# Main
if __name__ == '__main__':
    searcher = FrameSearcher()
    searcher.search_image('../../testing_images/trucks.jpg', 'red truck')