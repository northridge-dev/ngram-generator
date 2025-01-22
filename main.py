from model import NgramModel

def load_training_data():
    """
    Load multiple training text files and combine them into a single string.
    """
    files = ['train/great_gatsby.txt', 'train/pride_and_prejudice.txt', 'train/sherlock_holmes.txt']
    text = ""
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            text += f.read().replace('\n', ' ')
    return text

def main():
    # Load training data
    text = load_training_data()

    # Choose n-gram size and train model
    n = 4  # Use a 4-gram model for better context
    model = NgramModel(n)
    print("Training model...")
    model.train(text)

    # Generate text with different seeds
    seed_texts = ["the party was", "she looked at", "mr gatsby said", "it was a dark"]
    for seed in seed_texts:
        print(f"\nSeed: '{seed}'")
        generated_text = model.generate_text(seed, max_words=30, temperature=0.7)
        print(f"Generated Text: {generated_text}")
        print("-" * 50)

if __name__ == "__main__":
    main()
