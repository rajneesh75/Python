from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
load_dotenv()
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url="https://dbc-c379cba2-8489.cloud.databricks.com/ai-gateway/mlflow/v1"
)

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hello! How can I assist you today?"},
        {"role": "user", "content": "What is String theory?"},
    ],
    model="workspace.bronze.gptoss",
    max_tokens=1024
)

print(chat_completion.choices[0].message.content)

