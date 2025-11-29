from langchain_chroma import Chroma
from langchain_core.globals import set_debug, set_verbose
from langchain_openai import OpenAIEmbeddings


set_debug(True)
set_verbose(True)

embedding = OpenAIEmbeddings()
db = Chroma(collection_name="my_store", embedding_function=embedding,persist_directory="./chroma_storage")

print(db.get())