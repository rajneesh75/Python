import lamini
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("LAMINI.API_KEY"))
lamini.api_key = os.getenv("LAMINI.API_KEY")


llm = lamini.Lamini(
    model_name="meta-llama/Llama-2-7b-chat-hf",
)

non_instruct_output = llm.generate("Tell me how to train my dog to sit")
print("Not instruction-tuned output (Llama 2 Base):", non_instruct_output)