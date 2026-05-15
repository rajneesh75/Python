import os
from dotenv import load_dotenv
from huggingface_hub import login, InferenceClient


load_dotenv()
client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HUGGING_FACE_KEY")
)

response = client.chat_completion(
    model="deepseek-ai/DeepSeek-R1",
    messages=[
        {"role": "user", "content": "Are UFOs real?"}
    ],
    max_tokens=300
)

print(response.choices[0].message.content)