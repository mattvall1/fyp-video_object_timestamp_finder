# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Process text inputs and outputs
from nltk.corpus import wordnet # TODO: Check if we should use Open WordNet instead

class SearchTermHandler:
    def __init__(self, search_term):
        self.search_term = search_term

        # For the moment, just get word synonyms and print
        print("Synonyms for search term: ", self.get_word_synonyms(self.search_term))


    # Get synonyms for a word
    def get_word_synonyms(self, text):
        # Use WordNet to find synonyms
        synonyms = []
        for syn in wordnet.synsets(text):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())

        # Remove duplicates using a set and return
        return list(set(synonyms))

    def get_words_to_search(self):
        pass



