import grammar
import hmm
import hmm_hmmlearn

class Tagger:
    def __init__(self, grammar=grammar.Grammar(), textfile="", trainfile=""):
        self.terminals = []
        self.textfile = textfile
        self.trainfile = trainfile
        self.model = hmm_hmmlearn.HMModel(grammar)

    def train(self):
        with open(self.trainfile, "r") as f:
            lines = f.readlines()

        self.model.train(lines)

    def tag(self):
        self.model.tag(self.textfile)
