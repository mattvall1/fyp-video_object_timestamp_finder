# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script to test BLEU scoring
# Note: Download Conceptual Captions validation dataset from https://ai.google.com/research/ConceptualCaptions/download
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction


class BLEUScoring:
    def __init__(self, reference_captions, candidate_caption):
        # Check if the input is a list of captions or a string
        if isinstance(reference_captions, list):
            self.reference_caption = [
                reference_captions.split() for reference_captions in reference_captions
            ]
            print(f"Reference captions SPLIT: {self.reference_caption}")
        else:
            self.reference_caption = [reference_captions.split()]
        self.candidate_caption = candidate_caption.split()

    def get_sentence_bleu_score(self):
        # Create a smoothing function (Note: https://www.nltk.org/api/nltk.translate.bleu_score.html)
        smooth_f = SmoothingFunction()

        # Calculate BLEU score
        score = sentence_bleu(
            self.reference_caption,
            self.candidate_caption,
            smoothing_function=smooth_f.method2,
        )
        return score
