from datasets import load_dataset
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-70m")


def inference(text, model, tokenizer, max_input_tokens=1000, max_output_tokens=100):
    # Tokenize
    input_ids = tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=max_input_tokens)

    # Generate
    device = model.device
    generated_tokens_with_prompt = model.generate(input_ids=input_ids.to(device), max_length=max_output_tokens)

    # Decode
    generated_text_with_prompt = tokenizer.batch_decode(generated_tokens_with_prompt, skip_special_tokens=True)

    # Strip the prompt
    generated_text_answer = generated_text_with_prompt[0][len(text):]
    return generated_text_answer


finetuning_dataset_path = "lamini/lamini_docs"
finetuning_dataset = load_dataset(finetuning_dataset_path)
print('fine tuning dataset - {}'.format(finetuning_dataset))

test_sample = finetuning_dataset["test"][1]
print('test sample - {}'.format(test_sample))

print('inference - {}'.format(inference(test_sample["question"], model, tokenizer)))

instruction_model = AutoModelForCausalLM.from_pretrained("lamini/lamini_docs_finetuned")
print('inference1 - {}'.format(inference(test_sample["question"], instruction_model, tokenizer)))
