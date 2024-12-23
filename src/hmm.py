import grammar

class HMModel:
    def __init__(self, grammar):
        self.hidden_states = grammar.terminals
        self.trans_count = [[0 for _ in range(len(self.hidden_states))] for _ in range(len(self.hidden_states))]
        self.trans_prob = [[1 for _ in range(len(self.hidden_states))] for _ in range(len(self.hidden_states))]
        self.emit_count = []
        self.emit_prob = []
        self.start_count = [0 for _ in range(len(self.hidden_states))]
        self.start_prob = [1 for _ in range(len(self.hidden_states))]
        self.vocab = set()

    def train(self, datafile):
        f = open(datafile, 'r')
        for line in f:
            word, tag = line.strip().split()[0], line.strip().split()[1]


    def _process_word(self, word, tag):
        if self.emit_prob == []:
            self.emit_prob = [[1 for _ in range(len(self.hidden_states))] for _ in range(len(self.vocab))]
        if self.emit_count == []:
            self.emit_count = [[0 for _ in range(len(self.hidden_states))] for _ in range(len(self.vocab))]

        if word not in self.vocab:
            self.vocab.add(word)
            self.emit_count.append([0 for _ in range(len(self.hidden_states))])
            self.emit_prob.append([1 for _ in range(len(self.hidden_states))])

        self.emit_count[self.vocab.index(word)][self.hidden_states.index(tag)] += 1
        # TODO



