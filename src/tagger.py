import grammar
import perceptron
import string

class Tagger:
    def __init__(self, text):
        self.terminals = []
        self.textfiles = []
        self.text = text
        self.filedir = ""
        self.model = perceptron.Perceptron(n=0)

    def load_grammar(self, grammar: grammar.Grammar):
        filedir = grammar.filedir
        for terminal in grammar.terminals.keys():
            self.terminals.append(terminal)
            self.textfiles.append(filedir + grammar.terminals[terminal])

    def load_text(self, text):
        self.text = text

    def textfile_to_list(self, textfile):
        with open(textfile, 'r') as file:
            return file.read().splitlines()

    def tag(self):
        words = self.text.split()
        tagged = []
        for word in words:
            tag = self.model.predict(word)
            tagged.append((word, tag))
        return tagged


