import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"), transport="rest")

# Initialize the model
model = genai.GenerativeModel('gemini-2.5-pro')
priming_text = "Simulate you are Kapil Dev and bowling the last over of the match. " \
               "The opposing team need 6 runs to win."

question = "Tell me your chain of thoughts, strategy and tactics to prevent a win for opposing team. " \
           "Explain field placements"

decorator = "Also tell me the quality of my prompt and suggest me a better prompt, if any"
prompt = f"{priming_text} {question} {decorator}"


def GenerateText(prompt, model=model):
    print("Generating content...")

    # Generate text with a prompt
    response = model.generate_content(prompt)
    response.resolve()  # Wait for response
    return response.text


print(GenerateText(prompt))
