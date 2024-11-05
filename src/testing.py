import grammar 

# configure english grammar
grammar = grammar.Grammar()
grammar.add_terminal("noun", "nouns.txt")
grammar.add_terminal("verb", "verbs.txt")
grammar.add_terminal("preposition", "prepositions.txt")
grammar.add_terminal("determiner", "determiners.txt")
grammar.add_nonterminal("sentence")
grammar.add_nonterminal("noun_phrase")
grammar.add_nonterminal("verb_phrase")
grammar.add_nonterminal("prepositional_phrase")
grammar.add_nonterminal("sentence")
grammar.start = "sentence"
grammar.add_production("sentence", "noun_phrase verb_phrase")
grammar.add_production("noun_phrase", "determiner noun|determiner noun prepositional_phrase|noun|noun prepositional_phrase")
grammar.add_production("verb_phrase", "verb noun_phrase prepositional_phrase|verb noun_phrase|verb")
grammar.add_production("prepositional_phrase", "preposition noun_phrase")
grammar.print_grammar()
