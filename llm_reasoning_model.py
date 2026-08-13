import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging

logging.basicConfig(level=logging.DEBUG)
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.float32, local_files_only=True)
model.eval()

print("Model loaded.")
print("-" * 60)

question = """
A farmer has 17 sheep. All but 9 die.
How many sheep are left?
"""

prompt = f"""
Solve the following problem carefully.

{question}

Show your reasoning and then give the final answer.
"""

inputs = tokenizer(prompt, return_tensors="pt")
print("Generating...\n")

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.6, top_p=0.95, do_sample=True)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
