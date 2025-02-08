from nltk import tokenize, download
from nltk.data import find

# download the tokenizer model if not already downloaded
try:
    find('tokenizers/punkt')
except LookupError:
    download('punkt_tab')


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
    textbroke = []
    sentence = ''
    for letter in text:
        if letter != ' ' or sentence != '':
            sentence = sentence+letter 
        if letter == '.' or letter == '?' or letter == '!':
            if sentence[-3:] != 'Mr.' and sentence[-4:] != 'Mrs.' and sentence[-3:] != 'Dr.':
                sentence = sentence.replace('''
''', ' ')
                textbroke.append(sentence)
                sentence = ''
    if letter != '.' and letter != '?':
        textbroke.append(sentence)
    
    return textbroke


def word_tokenizer(sentence):
    """
    Strip punctuation, lowercase, and split a sentence 
    into words; return words in a list.
    """
    string = ''
    new_sentence = []
    for letter in sentence:
        if letter == ' ':
            if string != '':
                new_sentence.append(string)
                string = ''
        elif ord(letter) >= 65 and ord(letter) <= 90:
            letter = chr(ord(letter) + 32)
        if ord(letter) >= 97 and ord(letter) <= 122:
            string = string+letter
    if letter != ' ':
        new_sentence.append(string)
        
    return new_sentence
    


def build_ngrams(tokens, n):
    """
    This makes all the ngrams 
    """
    ngrams = []
    for i in range(len(tokens)+n-1):
        onegram = ()
        index = i-n+1
        for x in range(n):
            if index < 0:
                onegram = onegram + ('<s>',)
            elif index < len(tokens):
                onegram = onegram + (tokens[index],)
            else:
                onegram = onegram + ('</s>',)
            index += 1
        ngrams.append(onegram)
    return ngrams



def ngram_generator(text, n):
    """
    Creates a generator that yields n-grams of length n 
    from input text.
    """
    ngrams = []
    sentences = sentence_tokenizer(text) or []
    for sentence in sentences:
        tokens = word_tokenizer(sentence)
        for ngram in build_ngrams(tokens, n):
            ngrams.append(ngram)
    return ngrams