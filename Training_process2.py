import logging

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import Dataset
import json

logger = logging.getLogger(__name__)
global_config = None

dataset_name = "lamini_docs.jsonl"
dataset_path = dataset_name
use_hf = False
model_name = "EleutherAI/pythia-70m"

training_config = {"model": {"pretrained_name": model_name, "max_length": 2048},
                   "datasets": {"use_hf": use_hf, "path": dataset_path}, "verbose": True}

device_count = torch.cuda.device_count()
if device_count > 0:
    logger.debug("Select GPU device")
    device = torch.device("cuda")
else:
    logger.debug("Select CPU device")
    device = torch.device("cpu")


def inference(text, model, tokenizer, max_input_tokens=1000, max_output_tokens=100):
    # Tokenize
    input_ids = tokenizer.encode(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=max_input_tokens
    )

    # Generate
    device = model.device
    generated_tokens_with_prompt = model.generate(
        input_ids=input_ids.to(device),
        max_length=max_output_tokens
    )

    # Decode
    generated_text_with_prompt = tokenizer.batch_decode(generated_tokens_with_prompt, skip_special_tokens=True)

    # Strip the prompt
    generated_text_answer = generated_text_with_prompt[0][len(text):]

    return generated_text_answer


save_dir = 'lamini_docs_3_steps/final'
finetuned_slightly_model = AutoModelForCausalLM.from_pretrained(save_dir, local_files_only=True)
finetuned_slightly_model.to(device)


def tokenize_and_split_data(training_config, tokenizer):
    dataset_path = training_config["datasets"]["path"]
    max_length = training_config["model"]["max_length"]

    with open(dataset_path, "r") as f:
        data = [json.loads(line) for line in f]

    dataset = Dataset.from_list(data)

    def tokenize(examples):
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.truncation_side = "left"

        texts = []
        if "question" in examples and "answer" in examples:
            for q, a in zip(examples["question"], examples["answer"]):
                texts.append(q + a)
        elif "input" in examples and "output" in examples:
            for i, o in zip(examples["input"], examples["output"]):
                texts.append(i + o)
        elif "text" in examples:
            texts = examples["text"]
        else:
            raise KeyError(
                "Input data must contain either ('question' and 'answer'), ('input' and 'output'), or 'text' fields.")

        # Proper tokenization
        tokenized = tokenizer(texts, padding="max_length", truncation=True, max_length=2048)
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized

    tokenized_dataset = dataset.map(tokenize, batched=True, batch_size=1)
    split = tokenized_dataset.train_test_split(test_size=0.1)

    return split["train"], split["test"]


tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
train_dataset, test_dataset = tokenize_and_split_data(training_config, tokenizer)

test_question = test_dataset[0]['question']
print("Question input (test):", test_question)
print(f"Correct answer from Lamini docs: {test_dataset[0]['answer']}")
print("Finetuned slightly model's answer: ")
print(inference(test_question, finetuned_slightly_model, tokenizer))
