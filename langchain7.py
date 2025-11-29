from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(temperature=0.0, model="gpt-4.1-mini", api_key=os.getenv("OPENAI_API_KEY"), verbose=True)

product = "Queen Size Sheet Set"

# Step 2 — define transform from JSON to list and expand


def extract_names(output):
    match = re.search(r"\{.*\}", output, re.DOTALL)
    clean = match.group(0)
    data = json.loads(clean)
    return data["names"]


# prompt template 1
first_prompt = ChatPromptTemplate.from_template(
    "Give 10 company names for {product} in valid JSON: {\"names\":[...]}.")

# Prompt 2: generate description
second_prompt = ChatPromptTemplate.from_template("Write a 20 word description for the company: {name}")

# Step 3 — wrap into pipeline
pipeline = (
        first_prompt
        | llm
        | RunnableLambda(lambda msg: json.loads(re.search(r"\{.*\}", msg.content, re.DOTALL).group(0))["names"])
        | RunnableLambda(lambda names: [{"name": n} for n in names])
        | second_prompt.map()
        | llm.map()
)

result = pipeline.invoke({"product": product})

print("\n=== FINAL RESULT ===\n")
for name, desc in zip(extract_names(llm.invoke(first_prompt.invoke({"product": product})).content), result):
    print(f"{name}: {desc.content}")