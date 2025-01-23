from flask import Flask, render_template, request
from collections import defaultdict, Counter
import random
import re

app = Flask(__name__)

# Load training data
training_corpus = ['../train/great_gatsby.txt', '../train/pride_and_prejudice.txt', '../train/sherlock_holmes.txt', '../train/tale_of_two_cites.txt']
text = ""
for path in training_corpus:
    with open(path, 'r') as f:
        text += f.read()

def sentence_tokenizer(text):
    text = re.sub(r'[\u2018\u2019]', "'", text)
    text = re.sub(r'[\u201c\u201d]', '"', text)
    sentences = re.split(r'[.!?]', text)
    return [s.strip() for s in sentences if s.strip()]

def word_tokenizer(sentence):
    sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence.lower())
    return sentence.split()

class NgramModel:
    def __init__(self, n):
        self.n = n
        self.ngram_counts = defaultdict(Counter)
        self.lower_order_model = None

    def train(self, tokenized_sentences):
        for sentence in tokenized_sentences:
            padded_sentence = ['<s>'] * (self.n - 1) + sentence + ['</s>']
            for i in range(len(padded_sentence) - self.n + 1):
                ngram = tuple(padded_sentence[i:i + self.n - 1])
                next_word = padded_sentence[i + self.n - 1]
                self.ngram_counts[ngram][next_word] += 1
        if self.n > 1:
            self.lower_order_model = NgramModel(self.n - 1)
            self.lower_order_model.train(tokenized_sentences)

    def generate(self, seed, max_words=50):
        result = seed.split()
        for _ in range(max_words):
            context = tuple(result[-(self.n - 1):]) if len(result) >= self.n - 1 else tuple(result)
            next_word = self.predict_next(context)
            if next_word == '</s>':
                break
            result.append(next_word)
        return ' '.join(result)

    def predict_next(self, context):
        if context in self.ngram_counts:
            return max(self.ngram_counts[context], key=self.ngram_counts[context].get)
        elif self.lower_order_model:
            return self.lower_order_model.predict_next(context[1:])
        else:
            return random.choice(['the', 'a', 'an', 'is', 'was', 'Diddy'])

sentences = sentence_tokenizer(text)
tokenized_sentences = [word_tokenizer(sentence) for sentence in sentences]
model = NgramModel(n=3)
model.train(tokenized_sentences)

@app.route('/')
def index():
    return render_template('index.html', generated_text='')

@app.route('/generate', methods=['POST'])
def generate():
    seed = request.form['seed']
    generated_text = model.generate(seed)
    return render_template('index.html', generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)
