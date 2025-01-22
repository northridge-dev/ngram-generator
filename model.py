import random
from collections import defaultdict
from utils import sentence_tokenizer, word_tokenizer, build_ngrams

class NgramModel:
    def __init__(self, n):
        """
        Initialize the N-gram model with given size n.
        """
        self.n = n
        self.ngram_counts = defaultdict(int)
        self.context_counts = defaultdict(int)
        self.vocab = set()

    def train(self, text):
        """
        Train the N-gram model on the input text by counting n-grams.
        """
        sentences = sentence_tokenizer(text)
        for sentence in sentences:
            words = word_tokenizer(sentence)
            self.vocab.update(words)
            ngrams = build_ngrams(words, self.n)
            
            for ngram in ngrams:
                self.ngram_counts[ngram] += 1
                context = ngram[:-1]  # Get (n-1)-gram context
                self.context_counts[context] += 1

    def get_probability(self, ngram):
        """
        Calculate the probability of an n-gram given its (n-1)-gram context.
        Apply Laplace smoothing to avoid zero probabilities.
        """
        context = ngram[:-1]
        vocab_size = len(self.vocab)
        return (self.ngram_counts[ngram] + 1) / (self.context_counts[context] + vocab_size)

    def sample_next_word(self, possible_next_words, context, temperature=1.0):
        """
        Choose the next word based on adjusted probabilities using temperature control.
        """
        probabilities = [self.get_probability(context + (word,)) for word in possible_next_words]
        adjusted_probs = [p ** (1 / temperature) for p in probabilities]
        total_prob = sum(adjusted_probs)
        adjusted_probs = [p / total_prob for p in adjusted_probs]
        return random.choices(possible_next_words, weights=adjusted_probs)[0]

    def generate_text(self, seed, max_words=50, temperature=1.0):
        """
        Generate text using the trained N-gram model with temperature control.
        """
        if isinstance(seed, str):
            seed = word_tokenizer(seed)
        else:
            seed = list(seed)

        seed = ['<s>'] * (self.n - 1) + seed
        generated = seed[:]

        for _ in range(max_words):
            context = tuple(generated[-(self.n - 1):])
            possible_next_words = [
                ngram[-1] for ngram in self.ngram_counts if ngram[:-1] == context
            ]

            if not possible_next_words:
                break

            next_word = self.sample_next_word(possible_next_words, context, temperature)
            print(f"Context: {context} -> Next word: {next_word}")  # Debugging output

            if next_word == '</s>':
                break

            generated.append(next_word)

        return ' '.join(generated[self.n - 1:])
