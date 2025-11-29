from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(temperature=0.0, model="gpt-4.1-mini", api_key=os.getenv("OPENAI_API_KEY"), verbose=True)

product = "Queen Size Sheet Set"

# prompt template 1
first_prompt = ChatPromptTemplate.from_template(
    "What is the best name to describe a company that makes {product}?. "
    "Return only a JSON dictionary with format: {{'names': [ ... ]}}")

# Chain 1
chain_one = first_prompt | llm
output = chain_one.invoke({"product": product}).content
print("RAW OUTPUT:", output)

clean = re.sub(r"^```[a-zA-Z]*", "", output)
clean = clean.replace("```", "").strip()

result_dict = json.loads(clean)

print("\nDICTIONARY:")
print(result_dict)

# --- LLM #2 ---
second_prompt = ChatPromptTemplate.from_template(
    "Write a 20 word description for the following company: {name}"
)
chain_two = second_prompt | llm

print("\n--- DESCRIPTIONS ---")
for name in result_dict["names"]:
    desc = chain_two.invoke({"name": name}).content
    print(f"\n{name}:\n{desc}")
