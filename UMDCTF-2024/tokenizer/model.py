import sys
from transformers import AutoTokenizer

# Get the model name from the command line arguments
if len(sys.argv) > 1:
    model_name = sys.argv[1]
else:
    print("Usage: python script.py <model-name>")
    sys.exit(1)

# Load the tokenizer for the specified model
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Decode the tokens
tokens = [2864, 35, 1182, 37, 90, 28936, 8401, 821, 2957, 5677, 265, 7037, 40933, 29415, 92]
decoded_text = tokenizer.decode(tokens)

print(decoded_text)

