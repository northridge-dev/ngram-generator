from model import NgramLM

def ask():
    words = input('Write down two words ')
    word1 = ''
    word2 = ''
    wordlevel = 1
    for char in words:
        if char == ' ':
            wordlevel = 2
        else:
            if wordlevel == 1:
                word1 = word1 + char
            else:
                word2 = word2 + char
    return (word1, word2)

def main():
    # set n-gram size
    n = 3

    # choose texts to include in training
    gatsby = True
    pride_prejudice = True
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
        ngrams = model.train(text)
        words = ask()
        sentence = [words[0],words[1]]
        for i in range(12):
            list_of_next = model.generate(words, ngrams)
            if list_of_next != []:
                next_ngram = model.add_ngram(list_of_next)
                sentence.append(next_ngram)
                words = words[1]
                words = [words]
                words.append(next_ngram)
                words = (words[0], words[1])

        print(sentence)
    

if __name__ == '__main__':
    main()