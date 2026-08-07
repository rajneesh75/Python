from openai import OpenAI
import logging

logging.basicConfig(level=logging.DEBUG)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

completion = client.chat.completions.create(
    model="meta/llama-3.2-3b-instruct",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=False
)

print(completion.choices[0].message)
