import asyncio
import os
import sys

from air import DistillerClient
from air.utils import async_print
from dotenv import load_dotenv

load_dotenv()  # loads your API_KEY from your local '.env' file
api_key = str(os.getenv("AIREFINARY"))

# Force terminal to use UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')


async def main():
    """
    Runs the human-in-the-loop demo.
    """
    client = DistillerClient(api_key=api_key, verbose=True, debug=True)
    project_name = "human_in_the_loop_project"
    session_uuid = f"session_{os.getpid()}"

    client.create_project(config_path="config.yaml", project=project_name)

    async with client(project=project_name, uuid=session_uuid) as dc:
        query = "What are the latest advancements in LLMs?"
        responses = await dc.query(query=query)

        async for response in responses:
            print(f"\n{'='*50}")
            print(f"AGENT   : {response['role']}")
            print(f"CONTENT : {response['content']}")

            # Log to file for later inspection
            with open("agent_log.txt", "a") as f:
                f.write(f"\nAGENT: {response['role']}\n")
                f.write(f"CONTENT: {response['content']}\n")
                f.write("="*50 + "\n")

        await dc.reset_memory()
        await async_print("--- Session Complete ---")


if __name__ == "__main__":
    asyncio.run(main())
