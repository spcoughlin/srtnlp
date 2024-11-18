from . import grammar
import string

class CustomRule:
    def __init__(self, rule, token):
        self.rule = rule
        self.token = token

class Tokenizer:
    def __init__(self, text):
        self.terminals = []
        self.textfiles = []
        self.text = text
        self.filedir = ""
        self.custom_before_rules: list[CustomRule] = []
        self.custom_after_rules: list[CustomRule] = []

    def load_grammar(self, grammar: grammar.Grammar):
        filedir = grammar.filedir
        for terminal in grammar.terminals.keys():
            self.terminals.append(terminal)
            self.textfiles.append(filedir + grammar.terminals[terminal])

    def load_text(self, text):
        self.text = text

    def add_custom_before_rule(self, rule, token):
        self.custom_before_rules.append(CustomRule(rule, token))

    def add_custom_after_rule(self, rule, token):
        self.custom_after_rules.append(CustomRule(rule, token))

    def textfile_to_list(self, textfile):
        with open(textfile, 'r') as file:
            return file.read().splitlines()

    def search_textfile(self, target):
        for rule in self.custom_before_rules:
            if rule.rule(target):
                return rule.token

        for terminal, file in zip(self.terminals, self.textfiles):
            file = self.textfile_to_list(file)
            left, right = 0, len(file)
            while left < right:
                mid = left + (right - left) // 2
                if file[mid] == target.lower().strip(string.punctuation):
                    return terminal
                elif file[mid] < target.lower().strip(string.punctuation):
                    left = mid + 1
                else:
                    right = mid
        for rule in self.custom_after_rules:
            if rule.rule(target):
                return rule.token
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


