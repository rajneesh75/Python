from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")

text = "Hi, how are you?"
encoded_text = tokenizer(text)["input_ids"]
print(encoded_text)
decoded_text = tokenizer.decode(encoded_text)
print(decoded_text)