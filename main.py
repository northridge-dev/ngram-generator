from model import NgramLM

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
        model.train(text)

    # len = int(input())
    # seed_text = input()

    while True:
        seed_text = input()
        if seed_text == "/end":
            break

        print(" ".join(str(item) for item in model.generate(100,seed_text)))

    # for i in range(10):
    #     print(" ".join(str(item) for item in model.generate(100,seed_text)))
    #     seed_text = 

    # #print(model.generate(10,"Hello, I am"))
    # print(" ".join(str(item) for item in model.generate(100,seed_text))) 

if __name__ == '__main__':
    main()