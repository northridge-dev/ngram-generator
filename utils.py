from nltk import tokenize, download
from nltk.data import find

# download the tokenizer model if not already downloaded
try:
    find('tokenizers/punkt')
except LookupError:
    download('punkt')


def has_alphabetic(word):
    """
    Returns True if the input word has an alphabetic character.
    Use to filter out punctuation-only tokens.
    """
    return any(char.isalpha() for char in word)


def sentence_tokenizer(text):
    """
    Split input text into sentences; return them in a list
    NOTE: replaces "smart" quotations, apostrophes to more accurately
    split sentences
    """
    pass


def word_tokenizer(sentence):
    """
    Strip punctuation, lowercase, and split a sentence 
    into words; return words in a list.
    """
    pass


def build_ngrams(tokens, n):
    """
    From a list of tokens, build n-grams of size n, using
    <s> and </s> as start- and end-of-sentence markers.
    Ex: 
    tokens = ['the', 'cat', 'sat', 'on', 'the', 'mat']
    n = 3
    ngrams = [
        ('<s>', '<s>', 'the'), 
        ('<s>', 'the', 'cat'), 
        ('the', 'cat', 'sat'), 
        ...,   
        ('on', 'the', 'mat'), 
        ('the', 'mat', '</s>'),
        ('mat', '</s>', '</s>'),
    ]
    """
    pass


def ngram_generator(text, n):
    """
    Creates a generator that yields n-grams of length n 
    from input text.
    """
    sentences = sentence_tokenizer(text) or []
    for sentence in sentences:
        tokens = word_tokenizer(sentence)
        for ngram in build_ngrams(tokens, n):
            yield ngram