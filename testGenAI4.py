import os
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.oauth2.service_account import Credentials

logging.basicConfig(level=logging.INFO)

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("REGION")

if not PROJECT_ID:
    raise RuntimeError("PROJECT_ID not found")

if not LOCATION:
    raise RuntimeError("REGION not found")

KEY_PATH = r"C:\rock-sublime-446111-j0-749165cceca6.json"

credentials = Credentials.from_service_account_file(
    KEY_PATH,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    credentials=credentials,
)

prompt = """
Simulate you are Kapil Dev bowling the final over of a cricket match.
The opposing team needs 6 runs to win.

Describe:

1. Your bowling strategy.
2. Your field placements.
3. How you would try to prevent the opposition from winning.
4. Evaluate the quality of my prompt.
5. Suggest an improved version of my prompt.

Do not reveal internal reasoning or chain of thought. Instead, provide a concise explanation of your strategy.
"""

response = client.models.generate_content_stream(
    model="gemini-2.0-flash-exp",
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=8192,
    ),
)

print("\nResponse:\n")

for chunk in response:
    if chunk.text:
        print(chunk.text, end="", flush=True)
