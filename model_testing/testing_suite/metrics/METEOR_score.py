# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script for METEOR scoring
from nltk.translate import meteor


class METEORScoring:
    def __init__(self, reference_captions, candidate_caption):
        # Check if the input is a list of captions or a string
        if isinstance(reference_captions, list):
            self.reference_caption = [
                reference_captions.split() for reference_captions in reference_captions
            ]
        else:
            self.reference_caption = [reference_captions.split()]
        self.candidate_caption = candidate_caption.split()

    def get_meteor_score(self):
        # Calculate METEOR score
        score = meteor(self.reference_caption, self.candidate_caption)
        return round(score, 4)
