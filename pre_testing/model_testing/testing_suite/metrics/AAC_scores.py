# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script for AAC metrics scoring
import os
import subprocess
from aac_metrics import evaluate

# Force using Java 11
java_home = subprocess.check_output(['/usr/libexec/java_home', '-v', '11']).decode().strip()
os.environ['JAVA_HOME'] = java_home
os.environ['PATH'] = f"{os.path.join(java_home, 'bin')}:{os.environ['PATH']}"

# Install LMDB for SPICE metric
try:
    import ssl
    from aac_metrics.download import download_metrics

    ssl._create_default_https_context = ssl._create_unverified_context
    download_metrics()
except Exception as e:
    print(f"Warning: Error downloading metrics: {e}")


class AACScoring:
    def __init__(self, reference_captions, candidate_caption):
        # Ensure reference_captions is a list of lists
        if isinstance(reference_captions[0], str):
            self.reference_captions = [reference_captions]
        else:
            self.reference_captions = reference_captions

        self.candidate_caption = [candidate_caption]

    def get_cider_score(self):
        # Calculate CIDEr score
        corpus_scores, _ = evaluate(self.candidate_caption, self.reference_captions,
                                    metrics=['CIDEr'])

        # Extract CIDEr score
        cider_score = corpus_scores['CIDEr']

        # Return the CIDEr score
        return ["CIDEr", cider_score]

    def get_spice_score(self):
        # For SPICE, install LMDB first using Homebrew
        # brew install lmdb
        corpus_scores, _ = evaluate(self.candidate_caption, self.reference_captions,
                                    metrics=['SPICE'])

        # Extract SPICE score
        spice_score = corpus_scores['SPICE']

        # Return the SPICE score
        return ["SPICE", spice_score]


# Example usage
if __name__ == "__main__":
    reference_captions = ["A dog is running fast in the park"]
    candidate_caption = "A dog is running fast in the park"

    scorer = AACScoring(reference_captions, candidate_caption)

    # Test CIDEr
    try:
        cider_score = scorer.get_cider_score()
        print("CIDEr Score:", cider_score)
    except Exception as e:
        print(f"Error calculating CIDEr: {e}")

    # Test SPICE
    try:
        spice_score = scorer.get_spice_score()
        print("SPICE Score:", spice_score)
    except Exception as e:
        print(f"Error calculating SPICE: {e}")