from grammar import Grammar
from tagger import Tagger

# configure english grammar
grammar = Grammar("en")

# open the srt file
text = "the cats are on the mats"

# create a tagger object
tagger = Tagger(grammar, text, "pos.train.txt")
print("Training the model...")
tagger.train()
print("Tagging the text...")
print(tagger.tag())
