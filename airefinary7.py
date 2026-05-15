import asyncio
import os
import sys

from air import DistillerClient
from air.utils import async_print
from dotenv import load_dotenv

load_dotenv()  # loads your API_KEY from your local '.env' file
api_key = str(os.getenv("AIREFINARY"))


async def main():
    """
    Runs the human-in-the-loop demo.
    """
    client = DistillerClient(api_key=api_key, verbose=True, debug=True)
    project_name = "human_in_the_loop_project"
    session_uuid = f"session_{os.getpid()}"

    client.create_project(config_path="human.yaml", project=project_name)

    async with client(
            project=project_name,
            uuid=session_uuid
    ) as dc:
        query = "Do UFO's exist?"
        while True:
            responses = await dc.query(query=query)

            human_feedback = None
            async for response in responses:
                print(f"AGENT   : {response['role']}")
                print(f"CONTENT : {response['content']}")
                print(f"DEBUG role repr: {repr(response['role'])}")
                print(f"DEBUG full response: {repr(response)}")  # print the whole dict
                if response.status == 'requests':
                    human_feedback = input("\n[YOUR FEEDBACK]: ")
                    break  # exit the async for, then re-query below

            if human_feedback is None:
                break
            else:
                query = human_feedback  # feed back into next iteration

        await dc.reset_memory()
        await async_print("--- Session Complete ---")


if __name__ == "__main__":
    asyncio.run(main())
