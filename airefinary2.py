import asyncio
import os
from air import AsyncAIRefinery, DistillerClient
from dotenv import load_dotenv

load_dotenv()  # loads your API_KEY from your local '.env' file
api_key = str(os.getenv("AIREFINARY"))


async def simple_agent(query: str) -> str:
    # Your custom logic here
    return f"Data Scientist Agent response to: {query}"


async def quickstart_demo():
    distiller_client = DistillerClient(api_key=api_key)

    # Validate your configuration file before creating the project
    is_config_valid = distiller_client.validate_config(config_path="example.yaml")

    if not is_config_valid:
        # Abort if validation fails to avoid creating an invalid project
        print("Configuration validation failed!")
        return

    # upload your config file to register a new distiller project
    distiller_client.create_project(config_path="example.yaml", project="example")

    # Define a mapping between your custom agent to Callable.
    # When the custom agent is summoned by the super agent / orchestrator,
    # distiller-sdk will run the custom agent and send its response back to the
    # multi-agent system.
    executor_dict = {
        "Data Scientist Agent": simple_agent,
    }

    # connect to the created project
    async with distiller_client(
            project="example",
            uuid="rajneesh_uuid",
            executor_dict=executor_dict
    ) as dc:
        responses = await dc.query(query="Who won the FIFA world cup 2022?")  # send a query to project
        async for response in responses:
            print(response['content'])


if __name__ == "__main__":
    asyncio.run(quickstart_demo())
