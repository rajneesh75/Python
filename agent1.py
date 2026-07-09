import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


async def main() -> None:
    client = OpenAIChatCompletionClient(model="gpt-4o", api_key=os.environ["OPENAI_API_KEY"])

    try:
        agent = AssistantAgent("assistant", client)
        result = await agent.run(task="How are you")
        print(result)
        print("\nMESSAGES")

        for msg in result.messages:
            print(type(msg).__name__, ":", msg.content)

        print("\nFINAL ANSWER:")
        print(result.messages[-1].content)

    finally:
        await client.close()


asyncio.run(main())
