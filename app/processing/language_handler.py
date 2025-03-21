# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Process text inputs and outputs
import re
from nltk.corpus import wordnet  # TODO: Check if we should use Open WordNet instead


class LanguageHandler:
    def __init__(self, search_term):
        self.search_term = search_term

        # Get synonyms for the search term
        self.search_term_synonyms = self._get_search_synonyms()

    # Get search term
    def get_search_term(self):
        return self.search_term

    # Get synonyms for a word
    def _get_search_synonyms(self):
        # Use WordNet to find synonyms
        synonyms = []
        for syn in wordnet.synsets(self.search_term):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())

        # Remove duplicates using a set and return
        return set(synonyms)

    # Compare caption to search term
    def compare_caption_to_search_term(self, caption):
        # Get search term and split it into words
        split_caption = self._split_caption(caption)

        # Remove irrelevant words
        final_caption_words = self._remove_irrelevant_words(split_caption)

        # Get search term synonyms
        search_term_synonyms = self.search_term_synonyms

        # Check if any of the search term synonyms are in the caption
        intersection = search_term_synonyms & final_caption_words
        if intersection:
            return list(intersection)
        else:
            return False

    def _split_caption(self, caption):
        # Remove all punctuation and convert to lowercase (using regex)
        clean_caption = re.sub(r"[^\w\s]", "", caption.lower())

        # Split clean caption into individual words
        split_caption = clean_caption.split(" ")

        # Remove duplicates and return
        return set(split_caption)

    def _remove_irrelevant_words(self, word_set):
        # Define lists of irrelevant words (TODO: Make sure this is what we need to remove)
        pronouns = [
            "i",
            "me",
            "my",
            "you",
            "your",
            "he",
            "him",
            "his",
            "she",
            "her",
            "it",
            "its",
            "we",
            "us",
            "our",
            "they",
            "them",
            "their",
        ]
        conjunctions = [
            "and",
            "or",
            "but",
            "so",
            "for",
            "nor",
            "yet",
            "either",
            "neither",
        ]
        prepositions = [
            "in",
            "on",
            "at",
            "to",
            "with",
            "by",
            "for",
            "of",
            "about",
            "against",
            "between",
            "into",
            "through",
            "during",
            "before",
            "after",
        ]
        stop_words = [
            "a",
            "an",
            "the",
            "is",
            "are",
            "was",
            "were",
            "be",
            "being",
            "been",
            "am",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "doing",
            "will",
            "shall",
            "should",
            "can",
            "could",
            "may",
            "might",
        ]

        # Combine all irrelevant words into a single set
        all_irrelevant_words = set(pronouns + conjunctions + prepositions + stop_words)

        # Remove irrelevant words from the list
        relevant_words = word_set - all_irrelevant_words

        return relevant_words
