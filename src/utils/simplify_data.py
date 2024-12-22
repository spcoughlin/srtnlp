# English data:

# Confidence NN
# in IN
# the DT
# pound NN
# is VBZ
# widely RB
# expected VBN
# to TO
# take VB
# another DT
# sharp JJ
# dive NN
# if IN
# trade NN
# figures NNS
# for IN
# September NNP

# symbol_map:
#     old_symbol: new_symbol
#     means old symbol is replaced with new symbol for all words with old_symbol
import re

def simplify_data(file, symbol_map):
    with open(file, 'r') as f:
        lines = f.readlines()

    words = []
    symbols = []
    line_pattern = re.compile(r'^([a-zA-Z]+|%)+\s[A-Z]+$') # for converting from penn tagset
    for line in lines:
        if not line_pattern.match(line):
            words.append("BREAK")
            symbols.append("BREAK")
            continue
        word, symbol = line.split()
        words.append(word)
        symbols.append(symbol_map[symbol])

    with open(file, 'w') as f:
        for word, symbol in zip(words, symbols):
            f.write(f"{word} {symbol}\n")

def main():
    import sys
    n = len(sys.argv)
    if n != 2:
        print("Usage: python simplify_data.py <file>")
        sys.exit(1)

    file = sys.argv[1]

    # simplified penn tagset
    symbol_map = {
        'CC': 'CC',
        'CD': 'N',
        'DT': 'DT',
        'EX': 'V',
        'FW': 'N',
        'IN': 'PP',
        'JJ': 'A',
        'JJR': 'A',
        'JJS': 'A',
        'LS': 'N',
        'MD': 'V',
        'NN': 'N',
        'NNS': 'N',
        'NNP': 'N',
        'NNPS': 'N',
        'PDT': 'DT',
        'POS': 'N',
        'PRP': 'N',
        'PRP$': 'N',
        'RB': 'RB',
        'RBR': 'RB',
        'RBS': 'RB',
        'RP': 'V',
        'SYM': 'N',
        'TO': 'TO',
        'UH': 'N',
        'VB': 'V',
        'VBD': 'V',
        'VBG': 'V',
        'VBN': 'V',
        'VBP': 'V',
        'VBZ': 'V',
        'WDT': 'DT',
        'WP': 'N',
        'WP$': 'N',
        'WRB': 'RB',
        'BREAK': 'BREAK'
    }

    simplify_data(file, symbol_map)

if __name__ == '__main__':
    main()








