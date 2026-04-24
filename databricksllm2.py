from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("DATABRICKS_TOKEN"), base_url="https://dbc-c379cba2-8489.cloud.databricks.com/")

chat = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are an AI assistant"
        },
        {
            "role": "user",
            "content": "Tell me about Large Language Models"
        }
    ],
    model="databricks-llama-4-maverick",
)

print(chat.choices[0].message.content)
