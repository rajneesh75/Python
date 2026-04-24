import os
from air import AsyncAIRefinery, DistillerClient
from dotenv import load_dotenv

load_dotenv()  # loads your API_KEY from your local '.env' file
api_key = str(os.getenv("AIREFINARY"))

distiller_client = DistillerClient(api_key=api_key)

project = "party_project"

distiller_client.create_project(config_path="recommender.yaml", project=project)


async def recommender_agent(query: str) -> str:
    prompt = """Given the query below, your task is to provide the user with useful and cool
       recommendation followed by a one-sentence justification.\n\nQUERY: {query}"""

    prompt = prompt.format(query=query)

    airefinery_client = AsyncAIRefinery(api_key=api_key)

    response = await airefinery_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="openai/gpt-oss-120b",
    )

    return response.choices[0].message.content


executor_dict = {"Recommender Agent": recommender_agent}

response = distiller_client.interactive(
    project=project, uuid="rajneesh_uuid", executor_dict=executor_dict
)
