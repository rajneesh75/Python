import asyncio
import os
from air import AsyncAIRefinery  # a non-async AIRefinery client is also supported
from dotenv import load_dotenv

load_dotenv()  # loads your API_KEY from your local '.env' file
api_key = str(os.getenv("AIREFINARY"))


async def generate_response(query: str):
    # Initialize the AI Refinery client with authentication details
    client = AsyncAIRefinery(api_key=api_key)

    prompt = f"Your task is to generate a well formatted response based on the user query.\n\n{query}"

    # Request a chat completion through the client using the specified prompt and model
    response = await client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],  # Messages including the prompt for completion
        model="openai/gpt-oss-120b",  # Specify the model to use for generating the response
    )

    # Return the content of the first choice from the response
    return response.choices[0].message.content


# Example call to the generate_response function
if __name__ == "__main__":
    response = asyncio.run(
        generate_response("Pick a 15 member squad from the 1980s and 1990s era for a tour to australia."
                          "Keep a mix of experience and young talent. Include 2 wicket keepers."
                          "Explain your choices."))
    print(response)
