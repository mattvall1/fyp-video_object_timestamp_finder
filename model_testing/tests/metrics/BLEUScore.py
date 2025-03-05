# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script to test BLEU scoring
# Note: Download Conceptual Captions validation dataset from https://ai.google.com/research/ConceptualCaptions/download
from nltk.translate.bleu_score import sentence_bleu
import re


class BLEUScoring:
    def __init__(self, reference_caption, candidate_caption):
        self.reference_caption = [reference_caption.split()]
        self.candidate_caption = candidate_caption.split()

    def get_sentence_bleu_score(self):
        score = sentence_bleu(self.reference_caption, self.candidate_caption)
        return score
