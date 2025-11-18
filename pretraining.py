import jsonlines
import itertools
import pandas as pd
from pprint import pprint

import datasets
from datasets import load_dataset

pretrained_dataset = load_dataset("allenai/c4", "en", split="train", streaming=True, trust_remote_code=True)

n = 5
print("Pretrained dataset:")
top_n = itertools.islice(pretrained_dataset, n)
for i in top_n:
    print(i)


filename = "lamini_docs.jsonl"
instruction_dataset_df = pd.read_json(filename, lines=True)
#print(instruction_dataset_df)

examples = instruction_dataset_df.to_dict()
text = examples["question"][0] + examples["answer"][0]
print(text)

prompt_template_qa = """### Question:
{question}

### Answer:
{answer}"""

question = examples["question"][0]
answer = examples["answer"][0]

text_with_prompt_template = prompt_template_qa.format(question=question, answer=answer)
print(text_with_prompt_template)

prompt_template_q = """### Question:
{question}

### Answer:"""


num_examples = len(examples["question"])
finetuning_dataset_text_only = []
finetuning_dataset_question_answer = []
for i in range(num_examples):
    question = examples["question"][i]
    answer = examples["answer"][i]

    text_with_prompt_template_qa = prompt_template_qa.format(question=question, answer=answer)
    finetuning_dataset_text_only.append({"text": text_with_prompt_template_qa})

    text_with_prompt_template_q = prompt_template_q.format(question=question)
    finetuning_dataset_question_answer.append({"question": text_with_prompt_template_q, "answer": answer})

print(finetuning_dataset_text_only[0])
print(finetuning_dataset_question_answer[0])

with jsonlines.open(f'lamini_docs_processed.jsonl', 'w') as writer:
    writer.write_all(finetuning_dataset_question_answer)

#finetuning_dataset_name = "lamini/lamini_docs"
#finetuning_dataset = load_dataset(finetuning_dataset_name)
#print(finetuning_dataset)

finetuning_dataset = load_dataset("json", data_files="lamini_docs_processed.jsonl", split="train")
