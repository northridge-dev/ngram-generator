from model import NgramLM

def main():
    # set n-gram size
    n = 3

    # choose texts to include in training
    gatsby = True
    pride_prejudice = False
    sherlock = False

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
        model.train(text)

if __name__ == '__main__':
    main()