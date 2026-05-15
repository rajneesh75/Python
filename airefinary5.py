import os
from air import AsyncAIRefinery, DistillerClient
from dotenv import load_dotenv

load_dotenv()
api_key = str(os.getenv("AIREFINARY"))

PROJECT = "cricket"
CONFIG_PATH = "config.yaml"

distiller_client = DistillerClient(api_key=api_key)
distiller_client.create_project(config_path=CONFIG_PATH, project=PROJECT)


async def team_selection_agent(query: str) -> str:
    airefinery_client = AsyncAIRefinery(api_key=api_key)

    prompt = f"Query: {query}"

    response = await airefinery_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
    )
    print(response.choices[0].message.reasoning_content)
    return response.choices[0].message.content


async def captain_agent(query: str) -> str:
    prompt = f"Query: {query}"

    prompt = prompt.format(query=query)

    airefinery_client = AsyncAIRefinery(api_key=api_key)

    response = await airefinery_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="deepseek-ai/deepseek-r1-distill-qwen-32b", timeout=120
    )

    return response.choices[0].message.content


executor_dict = {"captain agent": captain_agent}

response = distiller_client.interactive(
    project=PROJECT, uuid="rajneesh", executor_dict=executor_dict
)
