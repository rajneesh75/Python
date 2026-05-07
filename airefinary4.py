import asyncio
import os
import time
from air import DistillerClient
from dotenv import load_dotenv

load_dotenv()  # loads your API_KEY from your local '.env' file
api_key = str(os.getenv("AIREFINARY"))


async def distiller_client_demo():
    distiller_client = DistillerClient(api_key=api_key)

    async with distiller_client(project="cricket", uuid="rajneesh", ) as dc:
        query = (
            "Indian cricket team is scheduled to go on a long tour to Australia in 1992 consisting of 5 test matches "
            "and a 3 nation ODI series just before the world cup. Pick a 16 member squad for the tour and justify"
            " your choices")
        responses = await dc.query(query=query)
        async for response in responses:
            print(f"[{time.strftime('%H:%M:%S')}] {response['content']}")


if __name__ == "__main__":
    asyncio.run(distiller_client_demo())
