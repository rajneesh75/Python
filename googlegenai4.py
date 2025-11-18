import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()


# Initialize the API client
genai.configure(api_key=os.getenv("API_KEY"), transport="rest")


def generate_text(prompt, model="gemini-2.5-pro"):
    try:
        # Initialize the model
        model = genai.GenerativeModel(model)
        print("Generating content...")
        response = model.generate_content(prompt, stream=True)
        response.resolve()  # Wait for response
        return response.text
    except Exception as e:
        return f"Error: {e}"


# Example usage
if __name__ == "__main__":
    prompt = "How are you."
    generated_text = generate_text(prompt)
    print("Generated Text:\n", generated_text)
