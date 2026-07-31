from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatBot:
    def __init__(self, system):
        print(f"__init__{system}")
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        print(f"__call__{message}")
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        print("execute..")
        completion = client.chat.completions.create(model="gpt-5.6", messages=self.messages)
        return completion.choices[0].message.content


simon = ChatBot("You are a helpful assistant who answers concisely")
result = simon("calculate: 4 * 7 / 3")
print(result)
