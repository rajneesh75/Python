import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv


load_dotenv()

LOCAL_REPO_PATH = "./my_local_repo"
COLLECTION_NAME = "python_code_embeddings"

# ---------------------------
# STEP 2 — Load all Python files recursively
# ---------------------------
documents = []
file_paths = []

for root, dirs, files in os.walk(LOCAL_REPO_PATH):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                print(path)
                print(content)
                documents.append(content)
                file_paths.append(path)
                print('-----------------')

print(f"Found {len(documents)} Python files")


# ---------------------------
# STEP 3 — Setup Chroma DB
# ---------------------------
print("Loading to chroma DB ...")
client = chromadb.PersistentClient(path="./my_chroma")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"   # Fast + good for code/text
)

# Delete existing collection if it exists
print("Deleting existing collection...")
client.delete_collection(name=COLLECTION_NAME)

print("Creating new collection...")
# Create new collection
collection = client.create_collection(name=COLLECTION_NAME,embedding_function=sentence_transformer_ef,)

# ---------------------------
# STEP 4 — Insert embeddings
# ---------------------------
ids = [str(i) for i in range(len(documents))]

collection.add(
    documents=documents,
    metadatas=[{"filepath": p} for p in file_paths],
    ids=ids
)

print(f"Inserted {len(documents)} documents into Chroma vector DB")