import unittest
from src import tokenize, grammar

class TestTokenizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the English grammar once for all tests
        cls.gram = grammar.Grammar("en")
    
    def test_tokenize_simple_sentence(self):
        """Test tokenizer on a simple sentence."""
        text = "the cat is on the table"
        expected_tokens = [
            ('the', 'determiner'),
            ('cat', 'noun'),
            ('is', 'verb'),
            ('on', 'preposition'),
            ('the', 'determiner'),
            ('table', 'noun')
        ]
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_tokenize_with_proper_noun(self):
        """Test tokenizer with proper nouns using custom after-rule."""
        text = "Alice went to Wonderland"
        expected_tokens = [
            ('Alice', 'propernoun'),
            ('went', 'verb'),
            ('to', 'preposition'),
            ('Wonderland', 'propernoun')
        ]
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        tokenizer.add_custom_after_rule(lambda x: x[0].isupper(), "propernoun")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_tokenize_complex_sentence(self):
        """Test tokenizer on a complex sentence covering various grammar rules."""
        text = "the quick brown fox jumps over the lazy dog"
        expected_tokens = [
            ('the', 'determiner'),
            ('quick', 'adjective'),
            ('brown', 'adjective'),
            ('fox', 'noun'),
            ('jumps', 'verb'),
            ('over', 'preposition'),
            ('the', 'determiner'),
            ('lazy', 'adjective'),
            ('dog', 'noun')
        ]
        
        # Update grammar to include adjectives
        self.gram.add_terminal('adjective', 'adjectives.txt')
        self.gram.add_nonterminal('adjective_phrase')
        self.gram.add_production('adjective_phrase', 'adjective|adjective adjective_phrase')
        self.gram.add_production('noun_phrase', 'adjective_phrase noun|adjective_phrase noun prepositional_phrase')
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_tokenize_with_unknown_words(self):
        """Test tokenizer with words not in grammar terminals."""
        text = "she sells seashells by the seashore"
        expected_tokens = [
            ('she', 'unknown'),
            ('sells', 'unknown'),
            ('seashells', 'unknown'),
            ('by', 'preposition'),
            ('the', 'determiner'),
            ('seashore', 'unknown')
        ]
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
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
    
    def test_tokenize_sentence_with_punctuation(self):
        """Test tokenizer handling punctuation."""
        text = "Hello, world!"
        expected_tokens = [
            ('Hello', 'interjection'),
            (',', 'punctuation'),
            ('world', 'noun'),
            ('!', 'punctuation')
        ]
        
        # Update grammar to include interjections and punctuation
        self.gram.add_terminal('interjection', 'interjections.txt')
        self.gram.add_terminal('punctuation', 'punctuation.txt')
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_tokenize_sentence_with_numbers(self):
        """Test tokenizer handling numbers."""
        text = "I have 2 apples and 3 oranges"
        expected_tokens = [
            ('I', 'unknown'),
            ('have', 'verb'),
            ('2', 'number'),
            ('apples', 'noun'),
            ('and', 'conjunction'),
            ('3', 'number'),
            ('oranges', 'noun')
        ]
        
        # Update grammar to include numbers and conjunctions
        self.gram.add_terminal('number', 'numbers.txt')
        self.gram.add_terminal('conjunction', 'conjunctions.txt')
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens, expected_tokens)

    def test_custom_before_rule(self):
        """Test custom before-rule for numbers."""
        text = "I have 2 apples and 3 oranges"
        expected_tokens = [
            ('I', 'unknown'),
            ('have', 'verb'),
            ('2', 'number'),
            ('apples', 'noun'),
            ('and', 'conjunction'),
            ('3', 'number'),
            ('oranges', 'noun')
        ]
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        # Custom before-rule for words that are numbers
        tokenizer.add_custom_before_rule(lambda x: x.isdigit(), "number")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens, expected_tokens)
    
    def test_custom_after_rule(self):
        """Test custom after-rule for proper nouns."""
        text = "Dr. Smith lives in New York City"
        expected_tokens = [
            ('Dr.', 'propernoun'),
            ('Smith', 'propernoun'),
            ('lives', 'verb'),
            ('in', 'preposition'),
            ('New', 'propernoun'),
            ('York', 'propernoun'),
            ('City', 'propernoun')
        ]
        
        tokenizer = tokenize.Tokenizer(text)
        tokenizer.load_grammar(self.gram)
        # Custom after-rule for words starting with uppercase letters
        tokenizer.add_custom_after_rule(lambda x: x[0].isupper(), "propernoun")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens, expected_tokens)

if __name__ == '__main__':
    unittest.main()

