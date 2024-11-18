import unittest
from src import grammar
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestGrammar(unittest.TestCase):
    def test_grammar_initialization(self):
        gram = grammar.Grammar("en")
        self.assertIsNotNone(gram)
        self.assertEqual(gram.start, 'sentence')
        self.assertIn('noun', gram.terminals)
        self.assertIn('sentence', gram.nonterminals)
        self.assertIn('sentence', gram.productions)
    
    def test_add_terminal(self):
        gram = grammar.Grammar()
        gram.add_terminal('adjective', 'adjectives.txt')
        self.assertIn('adjective', gram.terminals)
        self.assertEqual(gram.terminals['adjective'], 'adjectives.txt')
    
    def test_add_nonterminal(self):
        gram = grammar.Grammar()
        gram.add_nonterminal('adjective_phrase')
        self.assertIn('adjective_phrase', gram.nonterminals)
    
    def test_add_production(self):
        gram = grammar.Grammar()
        gram.add_nonterminal('noun_phrase')
        gram.add_terminal('adjective', 'adjectives.txt')
        gram.add_terminal('noun', 'nouns.txt')
        gram.add_production('noun_phrase', 'adjective noun')
        self.assertIn('noun_phrase', gram.productions)
        self.assertEqual(gram.productions['noun_phrase'], [['adjective noun']])
    
    def test_invalid_production(self):
        gram = grammar.Grammar()
        gram.add_nonterminal('noun_phrase')
        with self.assertRaises(ValueError):
            gram.add_production('noun_phrase', 'unknown_symbol noun')

    def test_set_start(self):
        gram = grammar.Grammar()
        gram.set_start('noun_phrase')
        self.assertEqual(gram.start, 'noun_phrase')
    
    def test_set_filedir(self):
        gram = grammar.Grammar()
        gram.set_filedir('english/')
        self.assertEqual(gram.filedir, 'english/')

if __name__ == '__main__':
    unittest.main()

