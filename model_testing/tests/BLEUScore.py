# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script to test BLEU scoring
# Note: Download Conceptual Captions validation dataset from https://ai.google.com/research/ConceptualCaptions/download
import evaluate
import re


class BLEUScoring:
    def __init__(self, reference_caption, candidate_caption):
        self.reference_caption = [reference_caption]
        self.candidate_caption = [candidate_caption]
        self.bleu = evaluate.load("bleu")

    def get_sentence_bleu_score(self):
        score = self.bleu.compute(
            predictions=self.candidate_caption, references=self.reference_caption
        )
        return score
