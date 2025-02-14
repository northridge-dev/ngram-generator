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

    def train(self, corpus):
        tokens = corpus.split()
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i : i + self.n])
            self.add_ngram(ngram)

    def add_ngram(self, ngram):
        node = self.root
        for word in ngram:
            if not node.has_child(word):
                node.add_child(TokenNode(word))
            node = node.get_child(word)

    def generate(self, length, seed_text):
        if seed_text is None:
            seed_text = random.choice(list(self.root.children.keys()))
        
        generated_tokens = seed_text.split()
        
        for _ in range(length):
            prev_tokens = tuple(generated_tokens[-(self.n - 1):])
            node = self.root
            for word in prev_tokens:
                if node.has_child(word):
                    node = node.get_child(word)
            
            if not node.children:
                break
            
            next_word = random.choices(
                list(node.children.keys())
            )[0]

            if not"Mrs."in next_word and not"Mr."in next_word and not"Dr."in next_word and '.' in next_word:
                generated_tokens.append(next_word)
                break

            generated_tokens.append(next_word)
        
        return generated_tokens