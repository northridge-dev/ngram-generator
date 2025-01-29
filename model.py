from utils import *

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

    def train(self, corpus):
        ngrams = ngram_generator(corpus, 3)
        return ngrams
        #print(ngrams[:10])

    # puts next word in the list
    def add_ngram(self, ngrams):
        counter = 0
        most_common = []
        for i in ngrams:
            most_common.append(1)
        for i in ngrams:
            for n in ngrams:
                if i == n:
                    most_common[counter] += 1
            counter += 1
        num = max(most_common)
        most_common = most_common.index(num)
        return ngrams[most_common]
                    
    # finds possible words 
    def generate(self, words, ngrams=None):
        count = 0
        list_of_next = []
        for gram in ngrams:
            if words == gram[:2] and gram[2] != '</s>':
                count += 1
                list_of_next.append(gram[2])
        return list_of_next