from google import genai
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How are you?"
)

print("Generating content...")
print(response.text)
