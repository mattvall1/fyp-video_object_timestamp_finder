# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script for ROUGE scoring
from rouge_score import rouge_scorer


class ROUGEScoring:
    def __init__(self, reference_captions, candidate_caption):
        # Check if the input is a list of captions or a string
        self.reference_caption = reference_captions
        self.candidate_caption = candidate_caption

    def get_rouge_score(self):
        # Create a ROUGE scorer
        rouge = rouge_scorer.RougeScorer(
            ["rouge1", "rouge2", "rougeL"],
            use_stemmer=True,
        )

        # Calculate ROUGE score for each reference caption (if multiple)
        scores = []
        for reference in self.reference_caption:
            # Calculate ROUGE score
            scores.append(rouge.score(reference, self.candidate_caption))

        # Average the F1 scores for each reference caption
        r1 = 0
        r2 = 0
        rl = 0
        for score in scores:
            r1 += score["rouge1"].fmeasure
            r2 += score["rouge2"].fmeasure
            rl += score["rougeL"].fmeasure

        return [
            ["ROUGE-1", r1 / len(scores)],
            ["ROUGE-2", r2 / len(scores)],
            ["ROUGE-L", rl / len(scores)],
        ]
