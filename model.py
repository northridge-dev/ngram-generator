from itertools import accumulate
from random import choices
from utils import ngram_generator, word_tokenizer

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
        generator = ngram_generator(corpus, self.n)
        for ngram in generator:
            self.add_ngram(ngram)

    def add_ngram(self, ngram):
        node = self.root
        for word in ngram:
            if not node.has_child(word):
                newNode = TokenNode(word)
                node.add_child(newNode)
            node.count += 1
            node = node.get_child(word)
        node.count += 1 # increment leaf node    


    def get_next_word(self, text):
        tokens = word_tokenizer(text)
        seed_tokens = tokens[-(self.n - 1):]
        node = self.root

        for word in seed_tokens:
            node = node.get_child(word) or self.get_random_child()
        
        vocabulary, cumulative_counts = self.get_word_count_lists(node)
        return choices(vocabulary, cum_weights=cumulative_counts)[0]
        
    
    def get_random_child(self):
        vocabulary, cumulative_counts = self.get_word_count_lists(self.root)
        # make a weighted choice
        choice = choices(vocabulary, cum_weights=cumulative_counts)[0]
        return self.root.get_child(choice)
    
    def get_word_count_lists(self, node):
        vocabulary = sorted(node.children.values(), key=lambda node: node.count, reverse=True)
        words = []
        counts = []
        for word_token in vocabulary:
            words.append(word_token.word)
            counts.append(word_token.count)

        return words, list(accumulate(counts))
    
    def generate(self, length, seed_text=None):
        generated_text = seed_text

        for _ in range(length):
            generated_text += " " + self.get_next_word(generated_text)
        
        return generated_text