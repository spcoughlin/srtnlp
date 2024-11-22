from grammar import Grammar
from tagger import Tagger
from perceptron import Perceptron

# configure english grammar
grammar = Grammar("en")

# open the srt file
text = "the cats are on the mats"

tagger = Tagger(text)
tagger.load_grammar(grammar)
tagger.model.load_grammar(grammar)
tagger.model.train()
tagged_text = tagger.tag()
for word, tag in tagged_text:
    print(f"{word}/({tag})", end=" ")
