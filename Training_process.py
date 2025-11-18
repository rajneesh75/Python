import lamini
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("LAMINI.API_KEY"))

lamini.api_key = os.getenv("LAMINI.API_KEY")

llm = lamini.Lamini(model_name="EleutherAI/pythia-410m", )
response = llm.generate("Tell me how to train my dog to sit.")

print('non dictionary output - {}'.format(response))

llm.upload_file("lamini_docs.jsonl", input_key="question", output_key="answer")
llm.train(data_or_dataset_id='66da58281b81219e55a579bf573c2b0bb6473a09955ec95a777339d4d1845e2b', is_public=True)
