import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

def predict_next_word(input_text, model, tokenizer, top_k=3):
    """
    Predicts the next word for a given input text.
    
    Args:
        input_text (str): The input text to predict the next word.
        model: Pretrained language model.
        tokenizer: Tokenizer corresponding to the model.
        top_k (int): Number of top predictions to return.
    
    Returns:
        List of tuples containing predicted words and their probabilities.
    """
    # Encode the input text
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    
    # Get model predictions
    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits
    
    # Get the logits for the last token
    last_token_logits = logits[0, -1, :]
    
    # Get the top-k predictions
    probabilities = torch.softmax(last_token_logits, dim=-1)
    top_k_probs, top_k_indices = torch.topk(probabilities, top_k)
    
    # Decode the top-k predictions
    predictions = [(tokenizer.decode([idx]), prob.item()) for idx, prob in zip(top_k_indices, top_k_probs)]
    return predictions

def complete_sentence(input_text, model, tokenizer, max_length=50):
    """
    Completes a sentence if the input consists of two words.
    
    Args:
        input_text (str): The input text to complete.
        model: Pretrained language model.
        tokenizer: Tokenizer corresponding to the model.
        max_length (int): Maximum length of the generated sentence.
    
    Returns:
        The completed sentence.
    """
    # Continue generating words until a punctuation mark or max_length is reached
    while len(input_text.split()) < max_length:
        predictions = predict_next_word(input_text, model, tokenizer, top_k=1)
        next_word = predictions[0][0].strip()
        input_text += f" {next_word}"
        
        # Stop if the next word is a punctuation mark (or ends with one)
        if next_word in [".", "!", "?"]:
            break
    
    return input_text

def main():
    # Load the pre-trained model and tokenizer
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    
    # Set the model to evaluation mode
    model.eval()
    
    # Input text
    input_text = input("Enter a sentence: ").strip()
    
    # Check if the input is short (2 words)
    if len(input_text.split()) <= 10:
        completed_sentence = complete_sentence(input_text, model, tokenizer)
        print("\nCompleted sentence:")
        print(completed_sentence)
    else:
        print("\nInput sentence is already longer than two words. No completion needed.")

if __name__ == "__main__":
    main()