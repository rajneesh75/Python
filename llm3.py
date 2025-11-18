from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from dotenv import load_dotenv

load_dotenv()

# model_name = "meta-llama/Llama-2-7b-hf"
model_name = "gpt2"


tokenizer = AutoTokenizer.from_pretrained(model_name, token=os.getenv("HUGGING_FACE_KEY"))
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, token=os.getenv("HUGGING_FACE_KEY"))
print("Model loaded successfully!")
print(tokenizer)
print(model)
