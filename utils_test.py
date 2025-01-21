import unittest
from utils import sentence_tokenizer, word_tokenizer, build_ngrams, ngram_generator

class TestUtils(unittest.TestCase):

    def test_sentence_tokenizer(self):
        text = "Hello world! This is a test."
        sentences = sentence_tokenizer(text)
        self.assertEqual(sentences, ["Hello world!", "This is a test."])

    def test_word_tokenizer(self):
        sentence = "Hello, world!"
        words = word_tokenizer(sentence)
        self.assertEqual(words, ["hello", "world"])

    def test_build_ngrams(self):
        tokens = ['the', 'cat', 'sat', 'on', 'the', 'mat']
        n = 3
        ngrams = build_ngrams(tokens, n)
        expected_ngrams = [
            ('<s>', '<s>', 'the'), 
            ('<s>', 'the', 'cat'), 
            ('the', 'cat', 'sat'), 
            ('cat', 'sat', 'on'), 
            ('sat', 'on', 'the'), 
            ('on', 'the', 'mat'), 
            ('the', 'mat', '</s>'),
            ('mat', '</s>', '</s>'),
        ]
        self.assertEqual(ngrams, expected_ngrams)

    def test_ngram_generator(self):
        text = "The cat sat on the mat."
        n = 3
        ngrams = list(ngram_generator(text, n) or [])
        expected_ngrams = [
            ('<s>', '<s>', 'the'), 
            ('<s>', 'the', 'cat'), 
            ('the', 'cat', 'sat'), 
            ('cat', 'sat', 'on'), 
            ('sat', 'on', 'the'), 
            ('on', 'the', 'mat'), 
            ('the', 'mat', '</s>'),
            ('mat', '</s>', '</s>'),
        ]
        self.assertEqual(ngrams, expected_ngrams)

if __name__ == '__main__':
    unittest.main()