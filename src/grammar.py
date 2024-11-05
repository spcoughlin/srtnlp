class Grammar:
    def __init__(self):
        self.terminals = {}
        self.nonterminals = set()
        self.productions = {}
        self.start = None

    def set_start(self, start: str):
        self.start = start

    def add_terminal(self, terminal: str, file: str):
        self.terminals[terminal] = file

    def add_terminal_group(self, terminals: dict):
        for terminal, file in terminals.items():
            self.add_terminal(terminal, file)

    def add_nonterminal(self, nonterminal: str):
        self.nonterminals.add(nonterminal)

    def add_nonterminal_group(self, nonterminals: set):
        for nonterminal in nonterminals:
            self.add_nonterminal(nonterminal)

    def add_production(self, nonterminal, production_str):
        if nonterminal not in self.nonterminals:
            raise ValueError(f"Nonterminal {nonterminal} not in grammar")
        # parse the production_str into all possible rules
        rules = production_str.split('|')
        for rule in rules:
            symbols = rule.split(' ')
            for symbol in symbols:
                if not (symbol in self.nonterminals or symbol in self.terminals.keys()):
                    raise ValueError(f"Specified symbol {symbol} not in grammar")
        if not self.productions.get(nonterminal):
            self.productions[nonterminal] = []
        self.productions[nonterminal].append(rules)

    def print_grammar(self):
        print("Terminals:")
        for terminal, file in self.terminals.items():
            print(f"{terminal} -> {file}")
        print("Nonterminals:")
        for nonterminal in self.nonterminals:
            print(nonterminal)
        print("Productions:")
        for nonterminal, rules in self.productions.items():
            print(f"{nonterminal} -> {rules}")



