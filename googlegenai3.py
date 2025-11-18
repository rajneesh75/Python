import os
import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"), transport="rest")

# Load and display an image
img = PIL.Image.open('books.jpg')

# Initialize the model
model = genai.GenerativeModel('gemini-2.5-pro')
prompt = "List the books described in picture"

print("Generating content...")
# Generate content from an image and prompt
response = model.generate_content([prompt, img], stream=True)
response.resolve()  # Wait for response
# Print the generated content
print(response.text)


