import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(temperature=0.0, model="gpt-4.1-mini", api_key=os.getenv("OPENAI_API_KEY"), verbose=True)

df = pd.read_csv('Data1.csv')
pd.set_option('display.max_colwidth', None)
print(df)

template = "Try to guess the name of company that makes {product}"
prompt_template = ChatPromptTemplate.from_template(template)
chain = prompt_template | llm
# Create list to store LLM outputs
results = []

# Loop through each row
for prod in df["Product"]:
    print(f"\n Asking LLM about product: {prod}")
    response = chain.invoke({"product": prod}).content
    results.append(response)

# Add new column to dataframe
df["company_guess"] = results

print("\nOUTPUT CSV With company guesses:")
print(df)
