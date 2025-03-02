# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Process captions to extract key phrases, note NLTK data must be downloaded: nltk.download()
import nltk
from rake_nltk import Rake
import os

class CaptionProcessor:
    def __init__(self):
        # Set NLTK data directory
        nltk_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "nltk_data")
        nltk.data.path.append(nltk_dir)

        # Initialize RAKE with WordNet 2022
        self.rake = Rake()

    def extract_key_phrases(self, text):
        self.rake.extract_keywords_from_text(text)
        ranked_phrases = self.rake.get_ranked_phrases()
        return ranked_phrases

# Example usage
if __name__ == "__main__":
    processor = CaptionProcessor()

    sample_text = ""
    key_words = processor.extract_key_phrases(sample_text)
    print(key_words)

    # print("Extracted key words:")
    # for word in key_words:
    #     print(f"- {word}")