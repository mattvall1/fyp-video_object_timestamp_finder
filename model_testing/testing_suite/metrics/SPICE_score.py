# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script for SPICE scoring
from pycocoevalcap.spice.spice import Spice


class SPICEScoring:
    def __init__(self, reference_captions, candidate_caption):
        # Check if the input is a list of captions or a string
        if isinstance(reference_captions, list):
            # Convert list of captions to a dictionary format
            self.gts = {0: reference_captions}
        else:
            self.gts = [reference_captions]
        # Convert candidate caption to a dictionary format
        self.res = {0: [candidate_caption]}

    def get_spice_score(self):
        print(self.gts)
        print(self.res)
        # Create a SPICE object
        spice = Spice()

        # Compute the score
        score, _ = spice.compute_score(self.gts, self.res)

        return score


if __name__ == "__main__":
    # Example usage
    reference_captions = ["A cat sitting on a couch.", "A cat on a sofa."]
    candidate_caption = "A cat sitting on a couch."

    spice_score = SPICEScoring(reference_captions, candidate_caption)
    print(spice_score.get_spice_score())
