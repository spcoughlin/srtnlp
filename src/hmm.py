import math
import grammar
from collections import defaultdict

class HMModel:
    def __init__(self, grammar=grammar.Grammar("en")):
        self.states = grammar.terminals if grammar.terminals else []
        self.transition_ps = defaultdict(lambda: defaultdict(float))
        self.emission_ps = defaultdict(lambda: defaultdict(float))
        self.start_p = defaultdict(float)
        self.tag_counts = defaultdict(int)
        self.transition_counts = defaultdict(lambda: defaultdict(int))
        self.emission_counts = defaultdict(lambda: defaultdict(int))
        self.start_counts = defaultdict(int)
        self.vocabulary = set()
        self.start_symbol = "<s>"

    # train the model
    def train(self, text):
        current_sentence_tags = []
        current_sentence_words = []
        for line in text:
            line = line.strip()
            if line == "BREAK BREAK":
                self._update_counts(current_sentence_words, current_sentence_tags)
                current_sentence_tags = []
                current_sentence_words = []
            else:
                if line:
                    word, pos = line.split()
                    current_sentence_tags.append(pos)
                    current_sentence_words.append(word)

        if current_sentence_tags:
            self._update_counts(current_sentence_words, current_sentence_tags)

        self._calculate_probabilities()

    # update counts for start, transition, and emission
    def _update_counts(self, words, tags):
        if tags:
            first_tag = tags[0]
            self.start_counts[first_tag] += 1
        prev_tag = self.start_symbol
        for word, tag in zip(words, tags):
            self.tag_counts[tag] += 1
            self.emission_counts[tag][word] += 1
            self.vocabulary.add(word)
            if prev_tag != self.start_symbol:
                self.transition_counts[prev_tag][tag] += 1
            prev_tag = tag
    
    # calculate probabilities for start, transition, and emission
    def _calculate_probabilities(self):
        total_sentences = sum(self.start_counts.values())
        for tag in self.start_counts:
            print(f"Start tag: {tag} Updated to {self.start_counts[tag] / total_sentences}")
            self.start_p[tag] = self.start_counts[tag] / total_sentences

        for prev_tag in self.transition_counts:
            total = sum(self.transition_counts[prev_tag].values())
            for curr_tag in self.transition_counts[prev_tag]:
                print(f"Transition: {prev_tag} -> {curr_tag} Updated to {self.transition_counts[prev_tag][curr_tag] / total}")
                self.transition_ps[prev_tag][curr_tag] = self.transition_counts[prev_tag][curr_tag] / total

        for tag in self.emission_counts:
            total = sum(self.emission_counts[tag].values())
            for word in self.emission_counts[tag]:
                print(f"Emission: {tag} -> {word} Updated to {self.emission_counts[tag][word] / total}")
                self.emission_ps[tag][word] = self.emission_counts[tag][word] / total

    # tag a sentence using the Viterbi algorithm
    def tag(self, sentence):
        return self._viterbi(sentence)

    # Viterbi algorithm
    def _viterbi(self, sentence):
        words = sentence.split()
        dp = [defaultdict(lambda: (-math.inf, None)) for _ in range(len(words) + 1)]
        for tag in self.states:
            first_word = words[0]
            log_init = math.log(self.start_p.get(tag, 1e-12)) if self.start_p else math.log(1e-12)
            emission = math.log(self.emission_ps[tag].get(first_word, 1e-12))
            dp[1][tag] = (log_init + emission, None)

        for i in range(2, len(words) + 1):
            word = words[i - 1]
            for curr_tag in self.states:
                curr_emission = math.log(self.emission_ps[curr_tag].get(word, 1e-12))
                best_score = -math.inf
                best_prev = None
                for prev_tag in self.states:
                    prev_score = dp[i - 1][prev_tag][0]
                    trans_p = math.log(self.transition_ps[prev_tag].get(curr_tag, 1e-12))
                    score = prev_score + trans_p + curr_emission
                    if score > best_score:
                        best_score = score
                        best_prev = prev_tag
                dp[i][curr_tag] = (best_score, best_prev)

        best_final_score = -math.inf
        best_final_tag = None
        for tag in self.states:
            if dp[len(words)][tag][0] > best_final_score:
                best_final_score = dp[len(words)][tag][0]
                best_final_tag = tag
        print(f"Best final tag: {best_final_tag}")
        print(words)

        best_path = []
        current_tag = best_final_tag
        for i in range(len(words), 0, -1):
            print(f"Best tag for {words[i - 1]}: {current_tag}")
            best_path.append(current_tag)
            current_tag = dp[i][current_tag][1]

        return best_path[::-1]



















