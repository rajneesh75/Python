import asyncio
import os
import time
from air import DistillerClient
from dotenv import load_dotenv


load_dotenv()  # loads your API_KEY from your local '.env' file
api_key = str(os.getenv("AIREFINARY"))


async def distiller_client_demo():
    distiller_client = DistillerClient(api_key=api_key)

    async with distiller_client(project="weather_project", uuid="rajneesh_uuid", ) as dc:
        responses = await dc.query(query="How is the weather today at Mountain View, California?"
                                   )  # send the query to be processed
        async for response in responses:
            print(f"[{time.strftime('%H:%M:%S')}] {response['content']}")


if __name__ == "__main__":
    asyncio.run(distiller_client_demo())
