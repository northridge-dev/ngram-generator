
text_easy = """
"He didn’t say any more, but we’ve always been unusually communicative
in a reserved way, and I understood that he meant a great deal more
than that. In consequence, I’m inclined to reserve all judgements, a
habit that has opened up many curious natures to me and also made me
the victim of not a few veteran bores. The abnormal mind is quick to
detect and attach itself to this quality when it appears in a normal
person, and so it came about that in college I was unjustly accused of
being a politician, because I was privy to the secret griefs of wild,
unknown men.
"""




class Tokenizer:
    def __init__(self):
        """
        Initialize the tokenizer for sentence tokenization.
        """
        pass

    def tokenize(self, text):
        """
        Tokenize the input text into sentences.
        :param text: The input string to tokenize.
        :return: A list of sentences.
        """
        import re
        
        # Normalize formatting by replacing newlines and excessive whitespace
        text = re.sub(r'[\n\r\t]+', ' ', text)
        text = re.sub(r'\s{2,}', ' ', text)
        
        # Define a pattern to match sentence boundaries
        sentence_pattern = r'(?<!\w\w\.[a-zA-Z])(?<![A-Z][a-z]\.)[.!?]\s+'
        
        # Split the text using the pattern
        sentences = re.split(sentence_pattern, text)
        return [sentence.strip() for sentence in sentences if sentence.strip()]

# Example usage:
if __name__ == "__main__":
    tokenizer = Tokenizer()
    text = text_easy
    sentences = tokenizer.tokenize(text)
    print(sentences)
