from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaConfig


# Step 1: Create a random config
config = LlamaConfig(
    hidden_size=512,
    intermediate_size=2048,
    num_attention_heads=8,
    num_hidden_layers=4,
    vocab_size=32000
)

# Step 2: Initialize a random model
model = AutoModelForCausalLM.from_config(config)

# Step 3: Load a tokenizer (can use any Llama tokenizer)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# Step 4: Random generation (it will output nonsense)
inputs = tokenizer("Tell me how to train my dog to sit.", return_tensors="pt")
outputs = model.generate(**inputs, max_length=50)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
