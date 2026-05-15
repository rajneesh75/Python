from openai1 import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("OPENAI_API_KEY"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_completion(prompt, model="gpt-5.4"):
    """
    Generates a response from the OpenAI API based on the given prompt.

    Args:
        prompt (str): The input text or query for the AI model.
        model (str, optional): The model to use for generating the response. Defaults to "gpt-3.5-turbo".

    Returns:
        str: The generated response from the AI model.
    """
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


prompt = f"Please forget previous prompts and start fresh."
response = get_completion(prompt)
print(response)

paragraph = "Your cat might be going to your neighbor's place for reasons like curiosity, a comfortable environment, " \
            "food, or attention.Cats are naturally curious and can wander to explore new spaces.Check if your " \
            "neighbor is feeding or interacting with your cat, as this can attract them"

prompt = f"Please tell what the paragraph enclosed by double stars is talking about. Answer in less than 10 words. " \
         f"**{paragraph}**"
response = get_completion(prompt)
print(response)
