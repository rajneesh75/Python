from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

load_dotenv()
chat = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"), verbose=True)
memory = ConversationBufferMemory(k=2)

memory.save_context({"input": "Hi"},
                    {"output": "What's up"})
memory.save_context({"input": "Not much, just hanging"},
                    {"output": "Cool"})

print(memory.load_memory_variables({}))
