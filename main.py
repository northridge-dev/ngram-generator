from model import NgramLM

def ask():
    words = input('Write down some words ')
    word = ''
    new_words = []
    for char in words:
        if char == ' ':
            new_words.append(word)
            word = ''
        else:
            word = word + char
    new_words.append(word)
    return new_words

def main():
    # set n-gram size
    n = 4

    # choose texts to include in training
    gatsby = False
    pride_prejudice = False
    sherlock = True

    # build corpus list
    training_corpus = []
    if gatsby:
        training_corpus.append('./train/great_gatsby.txt')
    if pride_prejudice:
        training_corpus.append('./train/pride_and_prejudice.txt')
    if sherlock:
        training_corpus.append('./train/sherlock_holmes.txt')


    model = NgramLM(n)
    for path in training_corpus:
        with open(path, 'r') as f:
            text = f.read()

        print(f'Training on {path}')
        ngrams = model.train(text, n)
        # gets list of starting words
        words = tuple(ask())
        sentence = list(words)
        new_words = []
        for i in range(n-1):
            new_words.append(words[-(n-i-1)])
        words = tuple(new_words)

        # adds words until its reached the end of the sentence
        while True:
            list_of_next = model.generate(words, ngrams, n)
            if list_of_next != []:
                next_ngram = model.add_ngram(list_of_next)
                sentence.append(next_ngram)
                if next_ngram == '.':
                    break
                words = list(words)
                words.pop(0)
                words.append(next_ngram)
                words = tuple(words)
            else:
                break
        
        # creates the sentence
        end_sentence = ""
        sentence[0] = sentence[0].capitalize()
        for i in sentence:
            if i == '.':
                end_sentence = end_sentence + i
            else:
                end_sentence = end_sentence + ' ' + i

        print(end_sentence)
    

if __name__ == '__main__':
    main()