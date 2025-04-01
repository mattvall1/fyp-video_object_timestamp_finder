# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script for SPICE scoring
from pycocoevalcap.spice.spice import Spice

# At the top of your file, add:
import os
os.environ['JAVA_HOME'] = '/Users/matthewvallance/Library/Java/JavaVirtualMachines/corretto-1.8.0_432/Contents/Home'
# Use the correct path from java_home -V output

class SPICEScoring:
    def __init__(self, reference_captions, candidate_caption):
        # Check if the input is a list of captions or a string
        self.reference_caption = reference_captions
        self.candidate_caption = candidate_caption
        
    def get_spice_score(self):

        # Create a SPICE scorer
        spice_scorer = Spice()

        # Prepare data for SPICE scorer (expects dictionary format)
        refs = {0: self.reference_caption}
        hypo = {0: [self.candidate_caption]}
        
        # Calculate SPICE score
        score, scores = spice_scorer.compute_score(refs, hypo)
        
        # Return the SPICE score in the same format as ROUGE
        return [["SPICE", round(score, 4)]]

# Example usage
if __name__ == "__main__":
    reference_captions = ["A dog is running in the park.", "A dog is playing with a ball."]
    candidate_caption = "A dog is playing."

    spice_scorer = SPICEScoring(reference_captions, candidate_caption)
    spice_score = spice_scorer.get_spice_score()

    print("SPICE Score:", spice_score)
