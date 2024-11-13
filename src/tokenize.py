import grammar

class Tokenizer:
    def __init__(self, text):
        self.terminals = []
        self.textfiles = []
        self.text = text

    def load_grammar(self, grammar):
        for terminal in grammar.terminals.keys():
            self.terminals.append(terminal)
            self.textfiles.append(grammar.terminals[terminal])

    def load_text(self, text):
        self.text = text

    def textfile_to_list(self, textfile):
        with open(textfile, 'r') as file:
            return file.read().splitlines()

    def search_textfile(self, target):
        for terminal, file in zip(self.terminals, self.textfiles):
            file = self.textfile_to_list(file)
            left, right = 0, len(file)
            while left < right:
                mid = left + (right - left) // 2
                if file[mid] == target:
                    return terminal
                elif file[mid] < target:
                    left = mid + 1
                else:
                    right = mid
        return None

    def tokenize(self):
        tokens = []
        text = self.text.split()
        for word in text:
            token = self.search_textfile(word)
            if token:
                tokens.append(token)
            else:
                tokens.append(word)
        return tokens


