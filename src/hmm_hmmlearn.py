import grammar
import numpy as np
from hmmlearn import hmm

class HMModel:
    def __init__(self, grammar=grammar.Grammar("en")):
        self.states = grammar.terminals if grammar.terminals else []
        self.state_to_id = {state: idx for idx, state in enumerate(self.states)}
        self.id_to_state = {idx: state for state, idx in self.state_to_id.items()}

        self.vocab = set()
        self.word_to_id = {}
        self.id_to_word = {}

        self.model = None

    def train(self, text):
        print("Training the model...")

        # Parse the training data into sentences
        sentences = []
        current_sentence_words = []
        for line_idx, line in enumerate(text):
            if line_idx % 100 == 0:
                print(f"Processing line {line_idx}...")

            line = line.strip()
            if line == "BREAK BREAK":
                if current_sentence_words:
                    sentences.append(current_sentence_words)
                current_sentence_words = []
            else:
                if line:
                    word, pos = line.split()
                    current_sentence_words.append(word)

        if current_sentence_words:
            sentences.append(current_sentence_words)

        # Build vocabulary
        print("Building vocabulary...")
        for sent in sentences:
            for w in sent:
                self.vocab.add(w)

        self.vocab = list(self.vocab)
        self.word_to_id = {w: i for i, w in enumerate(self.vocab)}
        self.id_to_word = {i: w for w, i in self.word_to_id.items()}

        n_components = len(self.states)
        n_features = len(self.vocab)

        # Convert sentences to one-hot encoded multinomial observations
        print("Converting sentences to one-hot encoded observations...")
        X = []
        lengths = []

        for sent_idx, sent in enumerate(sentences):
            if sent_idx % 50 == 0:
                print(f"Processing sentence {sent_idx}/{len(sentences)}...")

            obs_seq = []
            for w in sent:
                w_id = self.word_to_id[w]
                one_hot = np.zeros(n_features, dtype=int)
                one_hot[w_id] = 1
                obs_seq.append(one_hot)
            obs_seq = np.array(obs_seq)
            X.append(obs_seq)
            lengths.append(len(obs_seq))

        # Concatenate all sequences
        X = np.concatenate(X, axis=0)

        # Initialize MultinomialHMM
        print("Initializing the HMM model...")
        self.model = hmm.MultinomialHMM(n_components=n_components, n_iter=1000, tol=1e-4)

        # Fit the model
        print("Fitting the HMM model...")
        self.model.fit(X, lengths=lengths)

        print("Model trained.")
        print("Estimated start probabilities:", self.model.startprob_)
        print("Estimated transition matrix:", self.model.transmat_)

        max_words_to_print = 10
        for state_id, state in enumerate(self.states):
            print(f"Emission probabilities for state {state} (state_id={state_id}):")
            for w_id, prob in enumerate(self.model.emissionprob_[state_id][:max_words_to_print]):
                word = self.id_to_word[w_id]
                print(f"  {word}: {prob}")
            if n_features > max_words_to_print:
                print("  ...")

    def tag(self, sentence):
        print("Tagging the text...")
        words = sentence.split()
        n_features = len(self.vocab)

        # Convert to one-hot vectors
        print("Converting sentence to one-hot vectors...")
        obs_seq = []
        for w_idx, w in enumerate(words):
            if w_idx % 10 == 0:
                print(f"Processing word {w_idx}/{len(words)}...")

            w_id = self.word_to_id.get(w, None)
            one_hot = np.zeros(n_features, dtype=int)
            if w_id is not None:
                one_hot[w_id] = 1
            else:
                # For unknown words, place them into a known category arbitrarily (e.g., 0)
                # Ideally, you'd have a better unknown handling strategy.
                one_hot[0] = 1
            obs_seq.append(one_hot)
        obs_seq = np.array(obs_seq)

        # Decode
        print("Running Viterbi algorithm...")
        logprob, state_sequence = self.model.decode(obs_seq, algorithm="viterbi")
        print(f"Decoding complete. Log probability of the sequence: {logprob}")

        tag_sequence = [self.id_to_state[s] for s in state_sequence]

        print("Tagging results:")
        for word, tag in zip(words, tag_sequence):
            print(f"  {word}: {tag}")

        return tag_sequence

