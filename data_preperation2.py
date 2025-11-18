import pandas as pd
from pprint import pprint
from transformers import AutoTokenizer
import datasets

filename = "lamini_docs.jsonl"
instruction_dataset_df = pd.read_json(filename, lines=True)
examples = instruction_dataset_df.to_dict()

print(examples)

if "question" in examples and "answer" in examples:
    text = examples["question"][0] + examples["answer"][0]
elif "instruction" in examples and "response" in examples:
    text = examples["instruction"][0] + examples["response"][0]
elif "input" in examples and "output" in examples:
    text = examples["input"][0] + examples["output"][0]
else:
    text = examples["text"][0]

print(text)

prompt_template = """### Question:
{question}

### Answer:"""

num_examples = len(examples["question"])
finetuning_dataset = []

for i in range(num_examples):
    question = examples["question"][i]
    answer = examples["answer"][i]
    text_with_prompt_template = prompt_template.format(question=question)
    finetuning_dataset.append({"question": text_with_prompt_template, "answer": answer})

print("One datapoint in the finetuning dataset:")
pprint(finetuning_dataset[0])

text = finetuning_dataset[0]["question"] + finetuning_dataset[0]["answer"]
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")
tokenizer.pad_token = tokenizer.eos_token
tokenized_inputs = tokenizer(text, return_tensors="np", padding=True)
print(tokenized_inputs["input_ids"])

max_length = 2048
max_length = min(tokenized_inputs["input_ids"].shape[1], max_length, )

tokenized_inputs = tokenizer(text, return_tensors="np", truncation=True, max_length=max_length)

print(tokenized_inputs["input_ids"])


def tokenize_function(examples):
    if "question" in examples and "answer" in examples:
        text = examples["question"][0] + examples["answer"][0]
    elif "input" in examples and "output" in examples:
        text = examples["input"][0] + examples["output"][0]
    else:
        text = examples["text"][0]

    tokenizer.pad_token = tokenizer.eos_token
    tokenized_inputs = tokenizer(text, return_tensors="np", padding=True,)

    max_length = min(tokenized_inputs["input_ids"].shape[1], 2048)
    tokenizer.truncation_side = "left"
    tokenized_inputs = tokenizer(text, return_tensors="np", truncation=True, max_length=max_length)

    return tokenized_inputs


finetuning_dataset_loaded = datasets.load_dataset("json", data_files=filename, split="train")

tokenized_dataset = finetuning_dataset_loaded.map(
    tokenize_function,
    batched=True,
    batch_size=1,
    drop_last_batch=True
)

print(tokenized_dataset)

tokenized_dataset = tokenized_dataset.add_column("labels", tokenized_dataset["input_ids"])

split_dataset = tokenized_dataset.train_test_split(test_size=0.1, shuffle=True, seed=123)
print(split_dataset)
