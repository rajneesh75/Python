from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import vertexai
from vertexai.language_models import TextGenerationModel
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("PROJECT_ID"), os.getenv("REGION"))

# Path to your service account key file
key_path = 'c:\\rock-sublime-446111-j0-749165cceca6.json'

credentials = Credentials.from_service_account_file(key_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])

if credentials.expired:
    credentials.refresh(Request())

# initialize vertex
vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("REGION"), credentials=credentials)
print(vertexai.__version__)

generation_model = TextGenerationModel.from_pretrained("gemini-2.5-pro")

priming_text = "Simulate you are Kapil Dev and bowling the last over of the match. " \
               "The opposing team need 6 runs to win."

question = "Tell me your chain of thoughts, strategy and tactics to prevent a win for opposing team. " \
           "Explain field placements"

decorator = "Also tell me the quality of my prompt and suggest me a better prompt, if any"
prompt = f"{priming_text} {question} {decorator}"

print(generation_model.predict(prompt=prompt).text)
