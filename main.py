from model import NgramLM

def main():
    # set n-gram size
    n = 3

    # choose texts to include in training
    gatsby = False
    pride_prejudice = False
    sherlock = False
    totc = True
    other = True
    wolter = True

    # build corpus list
    training_corpus = []
    if gatsby:
        training_corpus.append('./train/great_gatsby.txt')
    if pride_prejudice:
        training_corpus.append('./train/pride_and_prejudice.txt')
    if sherlock:
        training_corpus.append('./train/sherlock_holmes.txt')
    if totc:
        training_corpus.append('./train/tale_of_two_cities.txt')
    if other:
        training_corpus.append('./train/other.txt')
    if wolter:
        training_corpus.append('./train/wolter.txt')


    model = NgramLM(n)
    for path in training_corpus:
        with open(path, 'r') as f:
            text = f.read()
        print(f'Training on {path}')
        model.train(text)
        # for node in model.root.children.values():
        #     print(node.word, node.count)

    generate_text = True
    length = 25
    while generate_text:
        seed = input(" >> ")
        if not seed:
            generate_text = False
        generated = model.generate(length, seed)
        print("---> "+generated[0].upper()+generated[1:])

if __name__ == '__main__':
    main()