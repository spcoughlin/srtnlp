class Grammar:
    def __init__(self, language=None):
        self.terminals = []
        self.nonterminals = []
        self.productions = {}
        self.start = None
        self.filedir = ""

        if language == "en":
            # Add terminals
            self.add_terminal_group(["noun", "verb", "preposition", "determiner", 
                                     "conjunction", "adjective", "adverb"])

            # Add nonterminals
            self.add_nonterminal_group(["sentence", "noun_phrase", "verb_phrase", 
                                        "prepositional_phrase", "adjective_phrase", 
                                        "adverb_phrase"])

            self.start = "sentence"

            # Ensure that there are no trailing spaces in these production rules
            self.add_production("sentence", "noun_phrase verb_phrase")
            self.add_production("sentence", "sentence conjunction sentence")

            # Noun phrase productions
            self.add_production("noun_phrase", 
                "determiner noun | "
                "determiner adjective_phrase noun | "
                "noun | "
                "adjective_phrase noun | "
                "noun_phrase prepositional_phrase | "
                "noun_phrase conjunction noun_phrase")

            # Verb phrase productions
            self.add_production("verb_phrase", 
                "verb | "
                "adverb_phrase verb | "
                "verb adverb_phrase | "
                "verb noun_phrase | "
                "verb_phrase prepositional_phrase | "
                "verb_phrase conjunction verb_phrase")

            # Prepositional phrase productions
            self.add_production("prepositional_phrase", "preposition noun_phrase")

            # Adjective phrase productions
            self.add_production("adjective_phrase", "adjective | adjective adjective_phrase")

            # Adverb phrase productions
            self.add_production("adverb_phrase", "adverb | adverb adverb_phrase")

    def set_start(self, start: str):
        self.start = start

    def add_terminal(self, terminal: str):
        self.terminals.append(terminal)

    def add_terminal_group(self, terminals: list):
        for terminal in terminals:
            self.add_terminal(terminal)

    def add_nonterminal(self, nonterminal: str):
        self.nonterminals.append(nonterminal)

    def add_nonterminal_group(self, nonterminals: list):
        for nonterminal in nonterminals:
            self.add_nonterminal(nonterminal)

    def add_production(self, nonterminal, production_str):
        if nonterminal not in self.nonterminals:
            raise ValueError(f"Nonterminal {nonterminal} not in grammar")
        # parse the production_str into all possible rules
        rules = production_str.split(' | ')
        for rule in rules:
            symbols = rule.split(' ')
            for symbol in symbols:
                if not (symbol in self.nonterminals or symbol in self.terminals):
                    raise ValueError(f"Specified symbol {symbol} not in grammar")
        if not self.productions.get(nonterminal):
            self.productions[nonterminal] = []
        self.productions[nonterminal].append(rules)

    def set_filedir(self, filedir: str):
        self.filedir = filedir

    def print_grammar(self):
        print("Terminals:")
        for terminal in self.terminals:
            print(f"{terminal}")
        print("Nonterminals:")
        for nonterminal in self.nonterminals:
            print(nonterminal)
        print("Productions:")
        for nonterminal, rules in self.productions.items():
            print(f"{nonterminal} -> {rules}")



