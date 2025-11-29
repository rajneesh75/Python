from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationChain



import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
print(llm)

memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

conversation.predict(input="Hi, my name is Rajneesh")
conversation.predict(input="What is 1+1?")
conversation.predict(input="What is my name?")

print('Memory buffer_____')
print(memory.buffer)

print('Memory variables_____')
print(memory.load_memory_variables({}))
memory = ConversationBufferMemory()
memory.save_context({"input": "Hi"},
                    {"output": "What's up"})

print('Memory buffer_____')
print(memory.buffer)
print(memory.load_memory_variables({}))
memory.save_context({"input": "Not much, just hanging"},
                    {"output": "Cool"})

print('Memory buffer_____')
print(memory.buffer)
print(memory.load_memory_variables({}))
