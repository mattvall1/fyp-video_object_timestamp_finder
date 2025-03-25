# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
"""Handles search term processing and text comparison."""
import re
from nltk.corpus import wordnet  # TODO: Check if we should use Open WordNet instead


class LanguageHandler:
    """Handles language processing tasks including synonym extraction and text comparison."""

    def __init__(self, search_term):
        self.search_term = search_term

        # Get synonyms for the search term
        self.search_term_synonyms = self._get_search_synonyms()

    def get_search_term(self):
        """
        Get the search term.

        Returns:
            str: The current search term
        """
        return self.search_term

    def _get_search_synonyms(self):
        """
        Get synonyms for the search term using WordNet.

        Returns:
            set: Set of synonyms for the search term
        """
        # Use WordNet to find synonyms
        synonyms = []
        for syn in wordnet.synsets(self.search_term):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())

        # Remove duplicates using a set and return
        return set(synonyms)

    def compare_caption_to_search_term(self, caption):
        """
        Compare caption to search term and its synonyms.

        Parameters:
            caption: Text caption to compare

        Returns:
            list or bool: List of matching terms if found, False otherwise
        """
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
        return False

    @staticmethod
    def _split_caption(caption):
        """
        Split caption into individual words after cleaning.

        Args:
            caption: Text caption to split

        Returns:
            set: Set of cleaned and split words
        """
        # Remove all punctuation and convert to lowercase (using regex)
        clean_caption = re.sub(r"[^\w\s]", "", caption.lower())

        # Split clean caption into individual words
        split_caption = clean_caption.split(" ")

        # Remove duplicates and return
        return set(split_caption)

    @staticmethod
    def _remove_irrelevant_words(word_set):
        """
        Remove irrelevant words from a set of words.

        Args:
            word_set: Set of words to filter

        Returns:
            set: Set of relevant words
        """
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
