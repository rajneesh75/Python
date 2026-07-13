from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
load_dotenv()
DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')

client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url="https://dbc-c379cba2-8489.cloud.databricks.com/ai-gateway/openai/v1",
    default_headers={"Databricks-Model-Provider-Service": "workspace.bronze.openai"}
)

response = client.responses.create(
    model="gpt-5.6",
    max_output_tokens=256,
    input=[
        {
            "role": "user",
            "content": [{"type": "input_text", "text": "Hello!"}]
        },
        {
            "role": "assistant",
            "content": [{"type": "output_text", "text": "Hello! How can I assist you today?"}]
        },
        {
            "role": "user",
            "content": [{"type": "input_text", "text": "What is Databricks?"}]
        }
    ]
)

print(response.output_text)
