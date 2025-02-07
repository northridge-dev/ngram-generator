from flask import Flask, render_template, request
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict, Counter
import os
import random

nltk.download('punkt')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './train'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#Main class for text generation
class NGramTextGenerator:
    #Configures global variables
    def __init__(self, n=3):
        self.n = n
        self.model = defaultdict(Counter)
    #Tokenizes
    def train(self, text):
        sentences = sent_tokenize(text.lower())
        for sentence in sentences:
            tokens = ['<s>'] * (self.n - 1) + word_tokenize(sentence) + ['</s>']
            for gram in ngrams(tokens, self.n):
                prefix, next_word = tuple(gram[:-1]), gram[-1]
                self.model[prefix][next_word] += 1
    
    def generate(self, seed_text, length=50):
        tokens = word_tokenize(seed_text.lower())
        if len(tokens) < self.n - 1:
            return "Seed text is too short."
        
        prefix = tuple(tokens[-(self.n-1):])
        result = list(prefix)
        
        for _ in range(length):
            if prefix not in self.model:
                break
            next_word = random.choices(list(self.model[prefix].keys()), 
                                       weights=self.model[prefix].values())[0]
            if next_word == '</s>':
                break
            result.append(next_word)
            prefix = tuple(result[-(self.n-1):])
        
        return ' '.join(result)

# Load and train the model

def load_training_corpus():
    training_text = ""
    train_directory = './train'
    for root, _, files in os.walk(train_directory):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    training_text += f.read() + " "
    return training_text

text_corpus = load_training_corpus()
generator = NGramTextGenerator(n=3)
generator.train(text_corpus)

@app.route('/')
def index():
    return render_template('index.html', generated_text='')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    generated_text = generator.generate(prompt)
    return render_template('index.html', generated_text=generated_text)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                new_text = f.read()
            global text_corpus, generator
            text_corpus += new_text
            generator.train(new_text)
        return render_template('index.html', generated_text='File uploaded and processed successfully.')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)