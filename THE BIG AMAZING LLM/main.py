from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict, Counter
import random
import re
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './train'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load training data
training_corpus = []
with open('training_files.txt', 'r') as file:
    training_corpus = [line.strip() for line in file if line.strip()]
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
            return random.choice(['the', 'a', 'an', 'is', 'was'])

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

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            with open(file_path, 'r') as f:
                new_text = f.read()
            global text, model
            text += new_text
            sentences = sentence_tokenizer(new_text)
            tokenized_sentences = [word_tokenizer(sentence) for sentence in sentences]
            model.train(tokenized_sentences)
        return render_template('index.html', generated_text='File uploaded and processed successfully.')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
