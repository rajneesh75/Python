import itertools
from datasets import load_dataset
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

pretrained_dataset = load_dataset("allenai/c4", "en", split="train", streaming=True, trust_remote_code=True)

n = 5
print("Pretrained dataset:")
top_n = itertools.islice(pretrained_dataset, n)
for i in top_n:
    print(i)

model_name = "meta-llama/Llama-2-7b-hf"  # Change for different models
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print(tokenizer)
print(model)
