from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("OPENAI_API_KEY"))

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_completion(role, prompt, model="gpt-3.5-turbo"):
    messages = [{"role": role, "content": prompt}]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


prompt = f"My name is Rajneesh. Can you remember it."
response = get_completion("system", prompt)
print(response)

prompt = f"My name is Rajneesh. Can you remember it. What is my name"
response = get_completion("user", prompt)
print(response)

