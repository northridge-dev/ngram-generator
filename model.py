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
        pass

    def add_ngram(self, ngram, count):
        pass

    def generate(self, length, seed_text=None):
        pass