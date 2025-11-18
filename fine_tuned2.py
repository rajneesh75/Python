import lamini
from datasets import load_dataset
import os
from dotenv import load_dotenv

load_dotenv()

lamini.api_key = os.getenv("LAMINI.API_KEY")
instruction_tuned_dataset = load_dataset("tatsu-lab/alpaca", split="train", streaming=True)
print('instruction_tuned_dataset - {}'.format(instruction_tuned_dataset))
