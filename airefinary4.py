import asyncio
import os
import time
from air import DistillerClient
from dotenv import load_dotenv


load_dotenv()  # loads your API_KEY from your local '.env' file
api_key = str(os.getenv("AIREFINARY"))


async def distiller_client_demo():
    distiller_client = DistillerClient(api_key=api_key)

    async with distiller_client(project="Cricket_ground", uuid="rajneesh_uuid", ) as dc:
        responses = await dc.query(query="Find a cricket ground in sector 12 in Dwarka")
        async for response in responses:
            print(f"[{time.strftime('%H:%M:%S')}] {response['content']}")


if __name__ == "__main__":
    asyncio.run(distiller_client_demo())
