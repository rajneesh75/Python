import google.generativeai as genai
from google.generativeai import types
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("PROJECT_ID"), os.getenv("REGION"))

key_path = 'c:\\rock-sublime-446111-j0-749165cceca6.json'
credentials = Credentials.from_service_account_file(key_path,
                                                    scopes=['https://www.googleapis.com/auth/cloud-platform'])
if credentials.expired:
    credentials.refresh(Request())

client = genai.client(vertexai=True, project=os.getenv("PROJECT_ID"), location=os.getenv("REGION"), credentials=credentials)

text1 = types.Part.from_text("""Simulate you are Kapil Dev and bowling the last over of the match. The opposing team need 6 runs to win. Tell me your chain of thoughts, 
        #strategy and tactics to prevent a win for opposing team. Explain field placements. Also tell me the quality of my prompt and suggest
        #me a better prompt, if any.""")


model = "gemini-2.0-flash-exp"
contents = [types.Content(role="user", parts=[text1])]
generate_content_config = types.GenerateContentConfig(temperature=1, top_p=0.95, max_output_tokens=8192,
                                                      response_modalities=["TEXT"])

response_text = ""
for chunk in client.models.generate_content_stream(model=model, contents=contents):
    # Extract only the text portion from each chunk
    if hasattr(chunk, "text"):
        response_text += chunk.text

# Print the clean response
print(response_text)