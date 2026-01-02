import requests
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("NVIDIA_API_KEY"))
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = False

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

headers = {
    "Authorization": "Bearer " + NVIDIA_API_KEY,
    "Accept": "text/event-stream" if stream else "application/json"
}

payload = {
    "model": "meta/llama-4-maverick-17b-128e-instruct",
    "messages": [{"role": "user", "content": "If I give you python source code would you be able to understand it?"}],
    "max_tokens": 512,
    "temperature": 1.00,
    "top_p": 1.00,
    "frequency_penalty": 0.00,
    "presence_penalty": 0.00,
    "stream": stream
}

response = requests.post(invoke_url, headers=headers, json=payload)

if stream:
    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))
else:
    print(response.json())
