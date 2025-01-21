# N-gram Text Generator

## Goal

Build and train a simple statistical language model that can generate plausible
text.

## Background

**N-gram** An n-gram is a run of _n_ words.

- unigram: `Python`
- bigram: `Python ain't`
- trigram: `Python ain't for`
- 4-gram: `Python ain't for sissies`

**N-gram Language Model** Language has measurable regularities. The likelihood
of a word appearing next in a text is conditioned by the words that precede it.
For example, try to think of ways to continue this text: `He fought`...
`valiantly`, `cancer`, `bravely`, `battles`, `against` are all reasonable
continuations and each is more likely than `lampshade`, `frugal`, `fought`, or
`He`.

A n-gram language model models these regularities.

**Simplifying Assumption (and Limitation) of N-gram Language Models** N-gram
language models are built by looking at existing text and counting the
frequencies of _n_-length sequences. From those frequencies, it is simple to
calculate for any _(n-1)_-length sequence what words are most likely to come
next.

For us humans, the larger _n_ is, the more likely we are to intelligently choose
the next word. `He fought` has many plausible continuations, but our choice
could push the sentence in very different directions. We stand a better chance
of finishing a longer sequence like
`He fought valiantly but could not forever withstand his enemy's`.

Not so an n-gram language model. 10-grams appear too infrequently to be modeled
well, even if we train our model on billions of words. Google's
[Ngram Viewer](https://books.google.com/ngrams/) fails to find a single example
of `He fought valiantly but could`. There are some techniques to "smooth out"
frequencies of longer n-grams, but the longer the sequences, the more likely the
model is to "over fit" the training data and reproduce verbatim phrases from the
training texts. Models with longer n-grams also require more computation and
memory. So in practice, _n_ tends to stay fairly small (<= 5 or 6). But that
means that the model has "forgotten" the beginning of all but the simplest
sentences when tasked with finishing them. Compare that to LLMs with a context
of at least 4000 words.

(Is it clear, then, that we humans don't generate text with some internal
n-gram-like frequency model?)

## High-Level Design

To build a model and use it to generate text, we need to:

- Pre-process training texts
  - read the training texts into memory
  - split the text into sentences
  - remove punctuation, convert to lowercase
  - "tokenize" the text (split it into words or word parts)
- Chunk the tokens into n-grams
  - break the pre-processed text into overlapping _n_-length chunks
- Train the model
  - count the frequency of each _n_-length chunk
  - store the counts so that we can readily access them
- Generate text
  - search the counts to find likely next words
  - use seed text to kick off a loop that uses the last _n_ words of generated
    text to choose a word that continues it.

## Components

### Training Texts

You'll use three public-domain books (from Project Gutenberg) to train the
n-gram model:

- _The Great Gatsby_ by F. Scott Fitzgerald
- _Pride and Prejudice_ by Jane Austen
- _The Adventures of Sherlock Holmes_ by Arthur Conan Doyle

You'll find these texts in the `train` directory.

### Tokenizers

In `utils.py`, you'll implement:

- `sentence_tokenizer`
- `word_tokenizer`

Use the function-level docstrings to guide your implementation. Use the VS Code
test runner to test your implementations.

### N-gram builder

Also in `utils.py`, you'll implement:

- `ngram_builder`

`ngram_generator` is already implemented. It uses the tokenizers and
`ngram_builder` to generate n-grams from the training texts.

Use the function-level docstrings to guide your implementation. Use the VS Code
test runner to test your implementations.

### N-gram language model

You'll implement the `NgramModel` class in `model.py`. It makes use of the
utilities you already implemented and an already-implemeted `TokenNode` class.

More details soon...
