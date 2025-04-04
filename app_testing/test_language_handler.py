# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Unit tests for the LanguageHandler class.

import unittest
from unittest.mock import MagicMock, patch
import os

from app.processing.language_handler import LanguageHandler


class TestLanguageHandler(unittest.TestCase):
    def setUp(self):
        # Set up patches for the WordNet components
        self.wordnet_patch = patch("app.processing.language_handler.wordnet")
        self.mock_wordnet = self.wordnet_patch.start()
        
        # Setup mock synsets and lemmas
        self.mock_lemma_1 = MagicMock()
        self.mock_lemma_1.name.return_value = "cat"
        
        self.mock_lemma_2 = MagicMock()
        self.mock_lemma_2.name.return_value = "feline"
        
        self.mock_lemma_3 = MagicMock()
        self.mock_lemma_3.name.return_value = "kitty"
        
        self.mock_synset_1 = MagicMock()
        self.mock_synset_1.lemmas.return_value = [self.mock_lemma_1, self.mock_lemma_2]
        
        self.mock_synset_2 = MagicMock()
        self.mock_synset_2.lemmas.return_value = [self.mock_lemma_3]
        
        # Set up wordnet to return mock synsets
        self.mock_wordnet.synsets.return_value = [self.mock_synset_1, self.mock_synset_2]
        
        # Create LanguageHandler instance with a test search term
        self.search_term = "cat"
        self.language_handler = LanguageHandler(self.search_term)
        
    def tearDown(self):
        # Stop patches
        self.wordnet_patch.stop()

    def test_init(self):
        # Test initialization
        self.assertEqual(self.language_handler.search_term, self.search_term)
        
        # Verify WordNet was used to find synonyms
        self.mock_wordnet.synsets.assert_called_once_with(self.search_term)
        
        # Verify synonyms were retrieved correctly
        expected_synonyms = {"cat", "feline", "kitty"}
        self.assertEqual(self.language_handler.search_term_synonyms, expected_synonyms)

    def test_get_search_synonyms(self):
        # Test _get_search_synonyms method
        synonyms = self.language_handler._get_search_synonyms()
        
        # Verify WordNet was called
        self.mock_wordnet.synsets.assert_called_with(self.search_term)
        
        # Verify synonyms are correctly extracted
        expected_synonyms = {"cat", "feline", "kitty"}
        self.assertEqual(synonyms, expected_synonyms)

    def test_split_caption(self):
        # Test _split_caption with various inputs
        test_cases = [
            # Plain text
            ("This is a cat", {"this", "is", "a", "cat"}),
            # With punctuation
            ("This is a cat!", {"this", "is", "a", "cat"}),
            # With mixed case
            ("This is a CAT", {"this", "is", "a", "cat"}),
            # With numbers and special characters
            ("A cat123 & mouse", {"a", "cat123", "mouse"}),
            # With duplicates
            ("cat cat cat", {"cat"}),
        ]
        
        for caption, expected in test_cases:
            result = LanguageHandler._split_caption(caption)
            self.assertEqual(result, expected)

    def test_remove_irrelevant_words(self):
        # Test _remove_irrelevant_words method with various inputs
        test_cases = [
            # Basic set with irrelevant words
            ({"cat", "in", "the", "park"}, {"cat", "park"}),
            # Set with only irrelevant words
            ({"in", "the", "for", "a"}, set()),
            # Set with no irrelevant words
            ({"cat", "mouse", "zebra"}, {"cat", "mouse", "zebra"}),
        ]
        
        for word_set, expected in test_cases:
            result = LanguageHandler._remove_irrelevant_words(word_set)
            self.assertEqual(result, expected)

    def test_compare_caption_to_search_term_with_match(self):
        # Set up test handler with known synonyms
        handler = self.language_handler
        handler.search_term_synonyms = {"cat", "feline", "kitty"}
        
        # Test captions that should match
        matching_captions = [
            "I have a cat at home",
            "The feline was meowing",
            "That's a beautiful kitty",
            "My CAT is very friendly",
            "She owns a feline and two hamsters"
        ]
        
        for caption in matching_captions:
            result = handler.compare_caption_to_search_term(caption)
            self.assertNotEqual(result, False, f"Failed to match caption: {caption}")
            self.assertIsInstance(result, list)
            self.assertTrue(len(result) > 0)

    def test_compare_caption_to_search_term_without_match(self):
        # Set up test handler with known synonyms
        handler = self.language_handler
        handler.search_term_synonyms = {"cat", "feline", "kitty"}
        
        # Test captions that should not match
        non_matching_captions = [
            "I have a dog at home",
            "The canine was barking",
            "That's a beautiful automobile",
            "My DOG is very friendly",
        ]
        
        for caption in non_matching_captions:
            result = handler.compare_caption_to_search_term(caption)
            self.assertEqual(result, False, f"Incorrectly matched caption: {caption}")

    def test_compare_caption_to_search_term_with_punctuation(self):
        # Set up test handler with known synonyms
        handler = self.language_handler
        handler.search_term_synonyms = {"cat", "feline", "kitty"}
        
        # Test captions with punctuation that should match
        caption = "I have a cat! It's very friendly."
        result = handler.compare_caption_to_search_term(caption)
        self.assertNotEqual(result, False)
        self.assertIn("cat", result)

    def test_compare_caption_with_irrelevant_words_only(self):
        # Set up test handler with known synonyms
        handler = self.language_handler
        handler.search_term_synonyms = {"cat", "feline", "kitty"}
        
        # Test caption with only irrelevant words (should not match)
        caption = "in the for a with by"
        result = handler.compare_caption_to_search_term(caption)
        self.assertEqual(result, False)

    def test_real_wordnet_lookups(self):
        # This test uses the actual WordNet (stop the patch)
        self.wordnet_patch.stop()
        
        # Test with a few common terms to verify integration with real WordNet
        for term in ["cat", "car", "house"]:
            handler = LanguageHandler(term)
            
            # Just verify we got some synonyms back from the real WordNet
            self.assertTrue(len(handler.search_term_synonyms) > 0)
            
            # Verify the original term is in the synonym set
            self.assertIn(term, handler.search_term_synonyms)
        
        # Restart the patch for other tests
        self.mock_wordnet = self.wordnet_patch.start()

    def test_compare_caption_with_multiple_matches(self):
        # Set up test handler with known synonyms
        handler = self.language_handler
        handler.search_term_synonyms = {"cat", "feline", "kitty"}
        
        # Test caption with multiple matches
        caption = "I have a cat and a kitty"
        result = handler.compare_caption_to_search_term(caption)
        
        # Verify we get both matches
        self.assertNotEqual(result, False)
        self.assertEqual(set(result), {"cat", "kitty"})

    
    def test_init_with_blank_search_term(self):
        # Test initialization with blank search term
        with self.assertRaises(ValueError):
            LanguageHandler("")
            
    def test_compare_caption_with_none_caption(self):
        # Test compare_caption_to_search_term with None caption
        with self.assertRaises(AttributeError):
            self.language_handler.compare_caption_to_search_term(None)
            
    def test_get_search_synonyms_with_wordnet_failure(self):
        # Test behavior when WordNet fails
        self.mock_wordnet.synsets.side_effect = Exception("WordNet error")
        
        # Expect the method to raise the exception
        with self.assertRaises(Exception):
            self.language_handler._get_search_synonyms()
            
    def test_split_caption_with_non_string_input(self):
        # Test _split_caption with non-string inputs
        test_cases = [
            123,               # Integer
            ["cat", "mouse"],    # List
            {"cat": "animal"}, # Dictionary
            None               # None
        ]
        
        for invalid_input in test_cases:
            with self.assertRaises(Exception):
                LanguageHandler._split_caption(invalid_input)
                
    def test_remove_irrelevant_words_with_non_set_input(self):
        # Test _remove_irrelevant_words with inputs that are not sets
        test_cases = [
            "cat mouse",         # String
            ["cat", "mouse"],    # List
            {"cat": "animal"}, # Dictionary
            123,               # Integer
            None               # None
        ]
        
        for invalid_input in test_cases:
            with self.assertRaises(Exception):
                LanguageHandler._remove_irrelevant_words(invalid_input)
                
    def test_compare_caption_with_very_large_caption(self):
        # Test compare_caption_to_search_term with very large caption
        # This tests performance with large inputs
        large_caption = " ".join(["word"] * 10000)  # 10,000 words
        
        # Should not throw exception and should return boolean result
        result = self.language_handler.compare_caption_to_search_term(large_caption)
        self.assertEqual(result, False)
        
    def test_compare_caption_with_special_characters_only(self):
        # Test with caption containing only special characters
        special_caption = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        # Should handle special characters and return False (no matches)
        result = self.language_handler.compare_caption_to_search_term(special_caption)
        self.assertEqual(result, False)

    def test_wordnet_returns_no_synsets(self):
        # Test behavior when WordNet returns no synsets
        # Create a new patch for this specific test
        with patch("app.processing.language_handler.wordnet") as mock_no_synsets:
            mock_no_synsets.synsets.return_value = []
            
            # Initialize with term that has no synonyms
            handler = LanguageHandler("nonexistentterm12345")
            
            # Should have only the search term itself (or empty if term is filtered out)
            self.assertEqual(handler.search_term_synonyms, set())
            
            # Compare should return False since there are no terms to match
            result = handler.compare_caption_to_search_term("This has no matches")
            self.assertEqual(result, False)
            
    def test_compare_caption_with_quoted_text(self):
        # Test with caption containing quoted text
        quoted_caption = '"My cat is named Whiskers," she said.'
        
        # Set up specific mock for this test
        handler = self.language_handler
        handler.search_term_synonyms = {"cat"}
        
        # Should extract "cat" and match it, ignoring quotes
        result = handler.compare_caption_to_search_term(quoted_caption)
        self.assertNotEqual(result, False)
        self.assertIn("cat", result)
