import asyncio
import os
from air import DistillerClient
from dotenv import load_dotenv

load_dotenv()  # loads your API_KEY from your local '.env' file
api_key = str(os.getenv("AIREFINARY"))


async def simple_agent(query: str) -> str:
    # Your custom logic here
    return f"Agent response : {query}"


async def quickstart_demo():
    distiller_client = DistillerClient(api_key=api_key)

    # Validate your configuration file before creating the project
    is_config_valid = distiller_client.validate_config(config_path="selection.yaml")

    if not is_config_valid:
        # Abort if validation fails to avoid creating an invalid project
        print("Configuration validation failed!")
        return

    # upload your config file to register a new distiller project
    distiller_client.create_project(config_path="selection.yaml", project="cricket")

    # Define a mapping between your custom agent to Callable.
    # When the custom agent is summoned by the super agent / orchestrator, distiller-sdk will run the
    # custom agent and send its response back to the multi-agent system.
    executor_dict = {"Team selector": simple_agent, }

    # connect to the created project
    async with distiller_client(project="cricket", uuid="rajneesh", executor_dict=executor_dict) as dc:
        query = "Pick a 17 member India squad from the 1990s era for a tour to australia."
        responses = await dc.query(query=query)
        async for response in responses:
            print(response['content'])

if __name__ == "__main__":
    asyncio.run(quickstart_demo())
