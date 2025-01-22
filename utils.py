import re
from collections import defaultdict

def sentence_tokenizer(text):
    """
    Split input text into sentences; return them in a list.
    Handles smart quotes and apostrophes.
    """
    text = text.replace('“', '"').replace('”', '"').replace("’", "'").replace("‘", "'")
    sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s')
    sentences = sentence_endings.split(text.strip())
    return [sentence.strip() for sentence in sentences if sentence]

def word_tokenizer(sentence):
    """
    Strip punctuation, lowercase, and split a sentence into words.
    """
    sentence = sentence.lower()
    sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)
    words = sentence.split()
    return words

def build_ngrams(tokens, n):
    """
    From a list of tokens, build n-grams of size n, using
    <s> and </s> as start- and end-of-sentence markers.
    """
    tokens = ['<s>'] * (n - 1) + tokens + ['</s>'] * (n - 1)
    ngrams = [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]
    return ngrams
