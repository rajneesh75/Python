from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
load_dotenv()
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url="https://dbc-c379cba2-8489.cloud.databricks.com/serving-endpoints"
)

response = client.chat.completions.create(
    model="databricks-meta-llama-3-1-8b-instruct",
    messages=[
        {
            "role": "user",
            "content": "what is string theory"
        }
    ],
    max_tokens=5000
)

print(response.choices[0].message.content)
