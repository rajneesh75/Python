from huggingface_hub import login
from huggingface_hub import HfApi
import os
from dotenv import load_dotenv

load_dotenv()
login(os.getenv("HUGGING_FACE_KEY"))


api = HfApi()
user_info = api.whoami(token=os.getenv("HUGGING_FACE_KEY"))
print(user_info)

files = api.list_repo_files("meta-llama/Llama-2-7b-hf")
print(files[:25])  # Print first few files

