import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"), transport="rest",)

# Initialize the model
model = genai.GenerativeModel('text-bison-001')
prompt = "How are you"

print("Generating content...")
# Generate content from an image and prompt
response = model.generate_content(prompt)

response.resolve()  # Wait for response

# Print the generated content
print(response.text)
