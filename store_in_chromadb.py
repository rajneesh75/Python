import chromadb
from chromadb.utils import embedding_functions

COLLECTION_NAME = "python_code_embeddings"


def read_local_repository_store_chromedb(documents, file_paths):
    print(f"Indexing {len(documents)} files into inmemory ChromaDB...")

    # client = chromadb.PersistentClient(path="./my_chroma")
    client = chromadb.Client()

    # Create embedding function
    embedder = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    # Create collection
    collection = client.create_collection(name=COLLECTION_NAME, embedding_function=embedder)

    # Prepare IDs
    ids = [str(i) for i in range(len(documents))]

    # Insert into Chroma
    collection.add(documents=documents, metadatas=[{"filepath": fp} for fp in file_paths], ids=ids)
    print(f"Inserted {len(documents)} documents into ChromaDB")
