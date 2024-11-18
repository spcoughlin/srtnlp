import unittest
from src import tokenize, grammar
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestTokenizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the English grammar once for all tests
        cls.gram = grammar.Grammar("en")
    
    def test_tokenize_simple_sentence(self):
        """Test tokenizer on a simple sentence."""
        text = "the cat is on the table"
        expected_tokens = ['determiner', 'noun', 'verb', 'preposition', 'determiner', 'noun']
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_tokenize_with_proper_noun(self):
        """Test tokenizer with proper nouns using custom after-rule."""
        text = "Alice went to Wonderland"
        expected_tokens = ['propernoun', 'verb', 'preposition', 'propernoun']
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        tokenizer.add_custom_after_rule(lambda x: x[0].isupper(), "propernoun")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_tokenize_empty_string(self):
        """Test tokenizer with empty string."""
        text = ""
        expected_tokens = []
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens, expected_tokens)

    def test_custom_before_rule(self):
        """Test custom before-rule for proper nouns."""
        text = "Smith lives in New York City"
        # "City" is classified as a proper noun, because the before rule checks the uppercase letter before the word list
        expected_tokens = ['propernoun', 'verb', 'preposition', 'propernoun', 'propernoun', 'propernoun']

        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        # Custom before-rule for words starting with uppercase letters
        tokenizer.add_custom_before_rule(lambda x: x[0].isupper(), "propernoun")
        tokens = tokenizer.tokenize()

        self.assertEqual(tokens, expected_tokens)
    
    def test_custom_after_rule(self):
        """Test custom after-rule for proper nouns."""
        text = "Smith lives in New York City"
        # "City" is classified as a noun, because the after rule checks the uppercase letter after the word list
        expected_tokens = ['propernoun', 'verb', 'preposition', 'propernoun', 'propernoun', 'noun']
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        # Custom after-rule for words starting with uppercase letters
        tokenizer.add_custom_after_rule(lambda x: x[0].isupper(), "propernoun")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens, expected_tokens)

if __name__ == '__main__':
    unittest.main()

