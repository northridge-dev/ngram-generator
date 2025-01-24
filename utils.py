from nltk import tokenize, download
from nltk.data import find

# download the tokenizer model if not already downloaded
try:
    find('tokenizers/punkt')
except LookupError:
    download('punkt_tab')
# download('punkt_tab')


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
    return tokenize.sent_tokenize(text.replace("“", '"').replace("’", "'").replace("”", '"').replace("‘", "'"))

t = "Hello. I am here now. Remy smells like Patrick making a wheel of indecipherable cheese with a rat’s tail! Does he really?"


def word_tokenizer(sentence):
    """
    Strip punctuation, lowercase, and split a sentence 
    into words; return words in a list.
    """
    words = tokenize.word_tokenize(sentence)
    return [word.lower() for word in words if has_alphabetic(word)]
# [el.lower() for el in sentence if el.isalpha()]


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
    for _ in range(n-1):
        tokens.append('</s>')
        tokens.insert(0, '<s>')

    sequences = []
    for i in range(n):
        sequences.append(tokens[i:])
        
    return zip(*sequences)


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