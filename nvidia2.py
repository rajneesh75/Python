from openai1 import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

completion = client.chat.completions.create(
    model="deepseek-ai/deepseek-r1",
    messages=[{"role": "user", "content": ""}],
    temperature=0.6,
    top_p=0.7,
    max_tokens=4096,
    stream=False
)

reasoning = getattr(completion.choices[0].message, "reasoning_content", None)
if reasoning:
    print(reasoning)
print(completion.choices[0].message.content)
