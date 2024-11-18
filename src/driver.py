import grammar 
import tokenize
import srt

# configure english grammar
grammar = grammar.Grammar("en")

# open the srt file
srtstr = srt.srt_text_to_string("example.srt")

# test tokenizer
tokenizer = tokenize.Tokenizer(srtstr)
tokenizer.load_grammar(grammar)
tokenizer.add_custom_after_rule(lambda x: x[0].isupper(), "propernoun")
print(f"Original text: {srtstr}")
print(f"Tokenized text: {tokenizer.tokenize()}")
