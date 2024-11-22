import grammar
from collections import defaultdict

class Perceptron:
    def __init__(self, n):
        self.terminals = []
        self.textfiles = []
        self.weights = {}    # Changed to a dictionary to hold feature weights per class
        self.bias = 0
        # Additional attributes for averaging
        self.totals = {}
        self.timestamps = {}
        self.i = 0           # Instance counter
        self.classes = set() # Set of POS tags (terminals)

    def load_grammar(self, grammar: grammar.Grammar):
        self.grammar = grammar  # Store the grammar for use in training
        filedir = grammar.filedir
        for terminal in grammar.terminals.keys():
            self.terminals.append(terminal)
            self.textfiles.append(filedir + grammar.terminals[terminal])
            self.classes.add(terminal)  # Collect all POS tags

    def train_word(self, word, true_class):
        # Increment instance counter
        self.i += 1
        # Extract features from the word
        features = self._get_features(word)
        # Predict the class
        pred_class = self.predict(word)
        # If prediction is incorrect, update weights
        if pred_class != true_class:
            self.update_weights(true_class, pred_class, features)

    # Train the perceptron to detect each terminal in the grammar based on provided wordlists
    def train(self):
        # Initialize additional structures if not already initialized
        if not hasattr(self, 'totals'):
            self.totals = {}
        if not hasattr(self, 'timestamps'):
            self.timestamps = {}
        if not hasattr(self, 'i'):
            self.i = 0

        # Load the grammar if not already loaded
        if not hasattr(self, 'grammar'):
            raise ValueError("Grammar not loaded. Please load the grammar before training.")

        wordlists = [self.grammar.filedir + self.grammar.terminals[terminal] for terminal in self.grammar.terminals.keys()]
        for wordlist, terminal in zip(wordlists, self.grammar.terminals.keys()):
            with open(wordlist, 'r', encoding='utf-8') as file:
                lines = file.read().splitlines()
                for word in lines:
                    self.train_word(word.strip(), terminal)

        # Average the weights after training
        self.average_weights()

    def predict(self, word):
        # Extract features from the word
        features = self._get_features(word)
        scores = defaultdict(float)
        for feat, value in features.items():
            if feat not in self.weights:
                continue
            weights = self.weights[feat]
            for clas, weight in weights.items():
                scores[clas] += value * weight
        # Return the class with the highest score
        if scores:
            return max(scores.items(), key=lambda item: (item[1], item[0]))[0]
        else:
            # Default to a class if no features matched
            return 'noun'

    # Helper method to extract features from a word
    def _get_features(self, word):
        features = {}
        word_lower = word.lower()
        features['bias'] = 1.0
        features['word.lower=' + word_lower] = 1.0
        # Prefixes and suffixes
        for i in range(1, 4):
            if len(word_lower) >= i:
                features['prefix' + str(i) + '=' + word_lower[:i]] = 1.0
                features['suffix' + str(i) + '=' + word_lower[-i:]] = 1.0
        features['word.len=%d' % len(word_lower)] = 1.0
        return features

    # Helper method to update weights
    def update_weights(self, true_class, pred_class, features):
        for feat, value in features.items():
            # Initialize weights and tracking structures if not present
            weights = self.weights.setdefault(feat, {})
            totals = self.totals.setdefault(feat, {})
            timestamps = self.timestamps.setdefault(feat, {})
            for clas in [true_class, pred_class]:
                if clas not in weights:
                    weights[clas] = 0.0
                    totals[clas] = 0.0
                    timestamps[clas] = 0
            # Update totals before updating weights
            for clas, adjustment in [(true_class, value), (pred_class, -value)]:
                delta = self.i - timestamps[feat][clas]
                totals[feat][clas] += delta * weights[feat][clas]
                timestamps[feat][clas] = self.i
                weights[feat][clas] += adjustment

    # Helper method to average weights after training
    def average_weights(self):
        for feat, weights in self.weights.items():
            new_weights = {}
            for clas, weight in weights.items():
                total = self.totals[feat][clas]
                delta = self.i - self.timestamps[feat][clas]
                total += delta * weight
                averaged = total / float(self.i)
                if averaged:
                    new_weights[clas] = averaged
            self.weights[feat] = new_weights

