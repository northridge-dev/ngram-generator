from utils import *
import random

class TokenNode:
    """
    A trie node that represents a word in the n-gram model.
    Stores a word, its count, and a dictionary of its children.
    """
    def __init__(self, word, count=0):
        self.word = word
        self.children = {}
        self.count = count

    def num_children(self):
        return len(self.children)
    
    def add_child(self, child):
        self.children[child.word] = child

    def has_child(self, word):
        return word in self.children
    
    def get_child(self, word):
        if self.has_child(word):
            return self.children[word]

class NgramLM:
    def __init__(self, n):
        self.n = n
        self.root = TokenNode('')

    def train(self, corpus, n):
        # makes a list of all the ngrams
        ngrams = ngram_generator(corpus, n)
        return ngrams
        #print(ngrams[:10])

    # puts next word in the list
    def add_ngram(self, ngrams):
        ngram = random.choice(ngrams)
        if ngram == '</s>':
            ngram = '.'
        return ngram
                    
    # finds possible words 
    def generate(self, words, ngrams, n):
        count = 0
        print(words, n)
        list_of_next = []
        for gram in ngrams:
            if words == gram[:(n-1)]:
                count += 1
                list_of_next.append(gram[(n-1)])
        return list_of_next