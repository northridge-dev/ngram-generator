from collections import defaultdict, Counter
import random
import re
input_text = input("Input text: ")
gatsby = True
pride_prejudice = True
sherlock = True
ToTC = True
text = ""

training_corpus = []
if gatsby:
        training_corpus.append('./train/great_gatsby.txt')
if pride_prejudice:
        training_corpus.append('./train/pride_and_prejudice.txt')
if sherlock:
        training_corpus.append('./train/sherlock_holmes.txt')
if ToTC:
     training_corpus.append('./train/tale_of_two_cites.txt')

for path in training_corpus:
        with open(path, 'r') as f:
            text = f.read()


class NgramModel:
    def __init__(self, n):
        self.n = n  # N-gram order
        self.ngram_counts = defaultdict(Counter)  # N-gram frequency counts
        self.lower_order_model = None  # Lower-order model for backoff

    def train(self, tokenized_sentences):
        """Train the model with tokenized sentences"""
        for sentence in tokenized_sentences:
            padded_sentence = ['<s>'] * (self.n - 1) + sentence + ['</s>']
            for i in range(len(padded_sentence) - self.n + 1):
                ngram = tuple(padded_sentence[i:i + self.n - 1])  # (n-1) prefix
                next_word = padded_sentence[i + self.n - 1]  # Next word
                self.ngram_counts[ngram][next_word] += 1
        
        # Train lower-order models for backoff
        if self.n > 1:
            self.lower_order_model = NgramModel(self.n - 1)
            self.lower_order_model.train(tokenized_sentences)

    def generate(self, seed, max_words=50):
        """Generate text based on the trained model."""
        result = seed.split()
        for _ in range(max_words):
            context = tuple(result[-(self.n - 1):]) if len(result) >= self.n - 1 else tuple(result)
            next_word = self.predict_next(context)
            if next_word == '</s>':
                break
            result.append(next_word)
        return ' '.join(result)

    def predict_next(self, context):
        """Predict the next word using backoff strategy."""
        if context in self.ngram_counts:
            return max(self.ngram_counts[context], key=self.ngram_counts[context].get)
        elif self.lower_order_model:
            return self.lower_order_model.predict_next(context[1:])
        else:
            return random.choice(['the', 'a', 'an', 'is', 'was',"Diddy"])  # Default fallback

def sentence_tokenizer(text):
    """Split input text into sentences."""
    text = re.sub(r'[\u2018\u2019]', "'", text)  # Convert smart quotes
    text = re.sub(r'[\u201c\u201d]', '"', text)
    sentences = re.split(r'[.!?]', text)
    return [s.strip() for s in sentences if s.strip()]

def word_tokenizer(sentence):
    """Tokenize a sentence into words."""
    sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence.lower())
    return sentence.split()

def build_ngrams(tokens, n):
    """Build n-grams with start and end markers."""
    tokens = ['<s>'] * (n - 1) + tokens + ['</s>']
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]

# Example usage
if __name__ == "__main__":
    sample_text = text
    sentences = sentence_tokenizer(sample_text)
    tokenized_sentences = [word_tokenizer(sentence) for sentence in sentences]
    
    model = NgramModel(n=3)
    model.train(tokenized_sentences)
    
    generated_text = model.generate(input_text)
    print(generated_text)