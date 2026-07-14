from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from vertexai.language_models import TextEmbeddingModel
from sklearn.metrics.pairwise import cosine_similarity
import vertexai
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
print("Loaded:", os.getenv("PROJECT_ID"), os.getenv("REGION"))

# Path to your service account key file
key_path = 'c:\\rock-sublime-446111-j0-749165cceca6.json'
credentials = Credentials.from_service_account_file(key_path,
                                                    scopes=['https://www.googleapis.com/auth/cloud-platform'])

if credentials.expired:
    credentials.refresh(Request())

# initialize vertex
vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("REGION"), credentials=credentials)
print(vertexai.__version__)

embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-005")

embedding1 = embedding_model.get_embeddings(["love"])
print(embedding1)
print('------------')
vector1 = [embedding1[0].values]
print(f"Length = {len(vector1)}")
print(vector1[:10])

embedding2 = embedding_model.get_embeddings(["what is love"])
vector2 = [embedding2[0].values]
print(f"Length = {len(vector2)}")
print(vector2[:10])

embedding3 = embedding_model.get_embeddings(["love is what"])
vector3 = [embedding3[0].values]
print(f"Length = {len(vector3)}")
print(vector3[:10])

print(cosine_similarity(vector1, vector2))
print(cosine_similarity(vector2, vector3))
print(cosine_similarity(vector3, vector1))
