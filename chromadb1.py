from langchain_chroma import Chroma
from langchain_core.globals import set_debug, set_verbose
from langchain_openai import OpenAIEmbeddings


set_debug(True)
set_verbose(True)

embedding = OpenAIEmbeddings()
db = Chroma(collection_name="my_store", embedding_function=embedding,persist_directory="./chroma_storage")

db.add_texts(["hello world"])
db.add_texts(["good morning"])
db.add_texts(["hola amigo"])
db.add_texts(["bye"])
db.add_texts(["Hi there"])

results = db.similarity_search_with_score("hello")
for doc, score in results:
    print(score, doc.page_content)
