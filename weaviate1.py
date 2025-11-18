import weaviate
from weaviate.classes.init import Auth
import weaviate.classes.config as wc
import weaviate.classes.query as wq
import pandas as pd
import requests
from datetime import datetime, timezone
import json
from weaviate.util import generate_uuid5
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("OPENAI_API_KEY"))

headers = {"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}  # Replace with your OpenAI API key
# Connect to Weaviate Cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url="https://dxiowfryrpqn26xpra.c0.asia-southeast1.gcp.weaviate.cloud/v1",
    auth_credentials=Auth.api_key(os.getenv("WEAVIATE_API_KEY")),
    headers=headers
)

print(client.is_ready())
print("Connection created.")

# resetting the schema. CAUTION: This will delete your collection
if client.collections.exists("Movie"):
    client.collections.delete("Movie")
    print("Existing collection deleted")

client.collections.create(
    name="Movie",
    properties=[
        wc.Property(name="title", data_type=wc.DataType.TEXT),
        wc.Property(name="overview", data_type=wc.DataType.TEXT),
        wc.Property(name="vote_average", data_type=wc.DataType.NUMBER),
        wc.Property(name="genre_ids", data_type=wc.DataType.INT_ARRAY),
        wc.Property(name="release_date", data_type=wc.DataType.DATE),
        wc.Property(name="tmdb_id", data_type=wc.DataType.INT),
    ],
    # Define the vectorizer module
    vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
    # Define the generative module
    generative_config=wc.Configure.Generative.openai()
)

print("Successfully created the schema.")

data_url = "https://raw.githubusercontent.com/weaviate-tutorials/edu-datasets/main/movies_data_1990_2024.json"
resp = requests.get(data_url)
df = pd.DataFrame(resp.json())
print("Movie dataframe created")

# Get the collection
movies = client.collections.get("Movie")

# Enter context manager
# with movies.batch.fixed_size(batch_size=10) as batch:
with movies.batch.dynamic() as batch:
    # Loop through the data
    for i, movie in tqdm(df.iterrows()):
        # Convert data types
        # Convert a JSON date to `datetime` and add time zone information
        release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        # Convert a JSON array to a list of integers
        genre_ids = json.loads(movie["genre_ids"])

        # Build the object payload
        movie_obj = {
            "title": movie["title"],
            "overview": movie["overview"],
            "vote_average": movie["vote_average"],
            "genre_ids": genre_ids,
            "release_date": release_date,
            "tmdb_id": movie["id"],
        }

        # Add object to batch queue
        batch.add_object(
            properties=movie_obj,
            uuid=generate_uuid5(movie["id"])
            # references=reference_obj  # You can add references here
        )
        # Batcher automatically sends batches

# Check for failed objects
if len(movies.batch.failed_objects) > 0:
    print(f"Failed to import {len(movies.batch.failed_objects)} objects")
else:
    print("Imported movie database")

print("Querying database")

# Perform query
response = movies.query.near_text(query="dystopian future", limit=2, return_metadata=wq.MetadataQuery(distance=True))

print(response)
# Inspect the response
for o in response.objects:
    print(
        o.properties["title"], o.properties["release_date"].year
    )  # Print the title and release year (note the release date is a datetime object)
    print(
        f"Distance to query: {o.metadata.distance:.3f}\n"
    )  # Print the distance of the object from the query

# Perform query
response = movies.query.near_text(query="dystopian future", limit=2, return_metadata=wq.MetadataQuery(distance=True))
filters = wq.Filter.by_property("release_date").less_than(datetime(1989, 1, 1))

print(response)
# Inspect the response
for o in response.objects:
    print(
        o.properties["title"], o.properties["release_date"].year
    )  # Print the title and release year (note the release date is a datetime object)
    print(
        f"Distance to query: {o.metadata.distance:.3f}\n"
    )  # Print the distance of the object from the query

# Perform query
response = movies.query.bm25(query="history", limit=2, return_metadata=wq.MetadataQuery(score=True))

print(response)
# Inspect the response
for o in response.objects:
    print(
        o.properties["title"], o.properties["release_date"].year
    )  # Print the title and release year (note the release date is a datetime object)
    print(
        f"BM25 score: {o.metadata.score:.3f}\n"
    )  # Print the BM25 score of the object from the query

response = movies.query.hybrid(query="history", limit=2, return_metadata=wq.MetadataQuery(score=True))

print(response)
# Inspect the response
for o in response.objects:
    print(
        o.properties["title"], o.properties["release_date"].year
    )  # Print the title and release year (note the release date is a datetime object)
    print(
        f"Hybrid score: {o.metadata.score:.3f}\n"
    )  # Print the hybrid search score of the object from the query

client.close()
