from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chat_completion = client.chat.completions.create(
    model="gpt-5.5",
    messages=[{"role": "user", "content": "Hello world"}]
)

print(chat_completion.choices[0].message.content)