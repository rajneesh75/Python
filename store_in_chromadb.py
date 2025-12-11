import chromadb
from chromadb.utils import embedding_functions
from tqdm import tqdm

COLLECTION_NAME = "python_code_embeddings"


def read_local_repository_store_chromedb(documents, file_paths):

    client = chromadb.Client()
    print(f"Loading embedder...")
    embedder = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=None)

    embeddings = []
    print("\nEmbedding documents with progress...\n")
    for doc in tqdm(documents, desc="Embedding"):
        embeddings.append(embedder([doc])[0])

    ids = [str(i) for i in range(len(documents))]
    metadatas = [{"filepath": fp} for fp in file_paths]

    print("\nAdding embeddings to ChromaDB...")
    collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

    print(f"\nInserted {collection.count()} documents into ChromaDB.")
    print("\nSample entry:", collection.get(ids=["0"]))
