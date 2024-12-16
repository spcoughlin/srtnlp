import grammar 
import tokenize

# configure english grammar
grammar = grammar.Grammar("en")

# test tokenizer
text = "the cats is on the mats"
tokenizer = tokenize.Tokenizer(text)
tokenizer.load_grammar(grammar)
print(f"Original text: {text}")
print(f"Tokenized text: {tokenizer.tokenize()}")
