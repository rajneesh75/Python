import asyncio
import os

from air import DistillerClient
from air.utils import async_print
from dotenv import load_dotenv

load_dotenv()  # loads your API_KEY from your local '.env' file
api_key = str(os.getenv("AIREFINARY"))

project = "Jammu_visit_project"


async def main():
    """
    Runs the customizable orchestrator demo.
    """
    # Initialize Distiller client, project name, and session id
    client = DistillerClient(api_key=api_key)
    project_name = "orchestrator_project"
    session_uuid = f"session_{os.getpid()}"

    # Initialize the orchestrator project
    client.create_project(config_path="orchestrator.yaml", project=project_name)

    async with client(project=project_name, uuid=session_uuid) as dc:
        query = ("Plan a 1-day trip to Jammu(India) by train for Saturday. "
                 "In Jammu, I also want to go to MAM stadium during the day."
                 " In evening I want to go to Hotel residency to have dinner.")
        responses = await dc.query(query=query)

        print(f"--- Running Query: {query} ---")
        async for response in responses:
            await async_print(
                f"Response from {response['role']}: {response['content']}"
            )

        # Clear session memory after the run
        await dc.reset_memory()
        await async_print("--- Session Complete ---")


if __name__ == "__main__":
    asyncio.run(main())
