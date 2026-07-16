import requests
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = False

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
headers = {
    "Authorization": "Bearer " + NVIDIA_API_KEY,
    "Accept": "text/event-stream" if stream else "application/json",
}
payload = {
    "messages": [
        {
            "role": "user",
            "content": "Hello world"
        }
    ],
    "model": "meta/llama-4-maverick-17b-128e-instruct",
    "frequency_penalty": 0,
    "max_tokens": 512,
    "presence_penalty": 0,
    "stream": stream,
    "temperature": 1,
    "top_p": 1
}

response = requests.post(invoke_url, headers=headers, json=payload, timeout=30, )

if stream:
    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))
else:
    print(response.json())
