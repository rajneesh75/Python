import lamini
import logging
import os
from dotenv import load_dotenv
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import Dataset
import json

load_dotenv()
print("Loaded:", os.getenv("LAMINI.API_KEY"))
lamini.api_key = os.getenv("LAMINI.API_KEY")
logger = logging.getLogger(__name__)
global_config = None



dataset_name = "lamini_docs.jsonl"
dataset_path = dataset_name
use_hf = False
model_name = "EleutherAI/pythia-70m"

training_config = {"model": {"pretrained_name": model_name, "max_length": 2048},
                   "datasets": {"use_hf": use_hf, "path": dataset_path}, "verbose": False}


def tokenize_and_split_data(training_config, tokenizer):
    dataset_path = training_config["datasets"]["path"]

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

print(train_dataset)
print(test_dataset)

base_model = AutoModelForCausalLM.from_pretrained(model_name)
device_count = torch.cuda.device_count()
if device_count > 0:
    logger.debug("Select GPU device")
    device = torch.device("cuda")
else:
    logger.debug("Select CPU device")
    device = torch.device("cpu")

base_model.to(device)


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


test_text = test_dataset[0]['question']
print("Question input (test):", test_text)
print(f"Correct answer from Lamini docs: {test_dataset[0]['answer']}")
print("Model's answer: ")
print(inference(test_text, base_model, tokenizer))

max_steps = 3

trained_model_name = f"lamini_docs_{max_steps}_steps"
output_dir = trained_model_name

training_args = TrainingArguments(

    # Learning rate
    learning_rate=1.0e-5,

    # Number of training epochs
    num_train_epochs=1,

    # Max steps to train for (each step is a batch of data)
    # Overrides num_train_epochs, if not -1
    max_steps=max_steps,

    # Batch size for training
    per_device_train_batch_size=1,

    # Directory to save model checkpoints
    output_dir=output_dir,

    # Other arguments
    overwrite_output_dir=False,  # Overwrite the content of the output directory
    disable_tqdm=False,  # Disable progress bars
    eval_steps=120,  # Number of update steps between two evaluations
    save_steps=120,  # After # steps model is saved
    warmup_steps=1,  # Number of warmup steps for learning rate scheduler
    per_device_eval_batch_size=1,  # Batch size for evaluation
    #evaluation_strategy="steps",
    logging_strategy="steps",
    logging_steps=1,
    optim="adafactor",
    gradient_accumulation_steps=4,
    gradient_checkpointing=False,

    # Parameters for early stopping
    load_best_model_at_end=True,
    save_total_limit=1,
    metric_for_best_model="eval_loss",
    greater_is_better=False
)

print(base_model)
print("Memory footprint", base_model.get_memory_footprint() / 1e9, "GB")

trainer = Trainer(model=base_model, args=training_args, train_dataset=train_dataset, eval_dataset=test_dataset, )

training_output = trainer.train()
save_dir = f'{output_dir}/final'
trainer.save_model(save_dir)
print("Saved model to:", save_dir)

finetuned_slightly_model = AutoModelForCausalLM.from_pretrained(save_dir, local_files_only=True)
finetuned_slightly_model.to(device)

test_question = test_dataset[0]['question']
print("Question input (test):", test_question)

print("Finetuned slightly model's answer: ")
print(inference(test_question, finetuned_slightly_model, tokenizer))
