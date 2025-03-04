# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script to run tests on models
from BLEUScore import BLEUScoring
from dataset_retrival.conceptual_captions import ConceptualCaptions

# Setup test
conceptual_captions = ConceptualCaptions()


if __name__ == "__main__":
    # Get all reference captions
    reference_captions = conceptual_captions.get_reference_captions()
    # Get all candidate captions (TODO: Get from OpenClip)
    candidate_captions = conceptual_captions.get_reference_captions()

    # Run BLEUScore tests for OpenClip
    for i in range(len(reference_captions)):
        bleu = BLEUScoring(reference_captions[i], candidate_captions[i])
        print(f"Sentence BLEU score: {bleu.get_sentence_bleu_score()}")

        if i == 10:
            break
