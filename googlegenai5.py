from transformers import pipeline

# Choose a pre-trained model for text generation
model_name = "gpt2"  # You can explore other options like "gpt-neo" or "facebook/bart-base"

# Initialize the pipeline for text generation
text_generator = pipeline("text-generation", model=model_name)

# Provide the starting prompt for text generation
prompt = "What is 2+2"

# Generate text with a maximum length of 50 words and temperature of 0.7 (controls creativity)
generated_text = text_generator(prompt, max_length=50, temperature=0.7)

# Print the generated text
print(generated_text[0]["generated_text"])