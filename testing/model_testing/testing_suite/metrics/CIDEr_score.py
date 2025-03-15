# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script to test CIDEr score
from pycocoevalcap.cider.cider import Cider


class CIDErScoring:
    def __init__(self, reference_caption, candidate_caption):
        self.reference_caption = {0: reference_caption}
        self.candidate_caption = {0: [candidate_caption]}

    def get_cider_score(self):
        # Create a Cider object
        cider = Cider()

        # Compute the score
        score, _ = cider.compute_score(self.reference_caption, self.candidate_caption)

        return score


if __name__ == "__main__":
    # Example usage
    reference_captions = ["A cat sitting on a couch.", "A cat on a sofa."]
    candidate_caption = "A cat sitting on a couch."

    cider_score = CIDErScoring(reference_captions, candidate_caption)
    print(cider_score.get_cider_score())
