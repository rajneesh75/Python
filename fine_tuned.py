import lamini
import os
from dotenv import load_dotenv

load_dotenv()

lamini.api_key = os.getenv("LAMINI.API_KEY")
llm = lamini.Lamini(model_name="meta-llama/Llama-3.1-8B-Instruct", )
response = llm.generate("Tell me how to train my dog to sit.")
print('non dictionary output - {}'.format(response))
