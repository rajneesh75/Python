import pandas as pd
from pprint import pprint
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")

filename = "lamini_docs.jsonl"

instruction_dataset_df = pd.read_json(filename, lines=True)
examples = instruction_dataset_df.to_dict()

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
tokenizer.pad_token = tokenizer.eos_token
tokenized_inputs = tokenizer(text, return_tensors="np", padding=True)

max_length = 2048
max_length = min(tokenized_inputs["input_ids"].shape[1], max_length, )

tokenized_inputs = tokenizer(text, return_tensors="np", truncation=True, max_length=max_length)
print(tokenized_inputs["input_ids"])