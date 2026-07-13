from openai import OpenAI
import os
import logging

logging.basicConfig(level=logging.DEBUG)
DATABRICKS_TOKEN = os.environ.get('DATABRICKS_TOKEN')


client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url="https://dbc-c379cba2-8489.cloud.databricks.com/serving-endpoints"
)

response = client.chat.completions.create(
    model="workspace.bronze.gpt56",
    messages=[
        {
            "role": "user",
            "content": "What is an LLM agent?"
        }
    ],
    max_tokens=5000
)

print(response.choices[0].message.content)