import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
from jira import JIRA
import logging
from openai import OpenAI

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

LOCAL_REPO_PATH = "./my_local_repo"
COLLECTION_NAME = "python_code_embeddings"

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_KEY")
ISSUE_KEY = os.getenv("ISSUE_KEY")

print("Reading chroma DB...")
client = chromadb.PersistentClient(path="./my_chroma")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"  # Fast + good for code/text
)

collection = client.get_collection(name=COLLECTION_NAME, embedding_function=sentence_transformer_ef, )
query = "Modify the script that returns the sum of 2 numbers to instead return a sum of 3 numbers."
results = collection.query(query_texts=[query], n_results=3)

print("Possible matching scripts:")
for idx, (doc, meta, score) in enumerate(
        zip(results["documents"][0], results["metadatas"][0], results["distances"][0])):
    print(f"{idx + 1}. File: {meta.get('filepath')}  Score: {score}")
    print(doc[:150])
    print("-----")

prompt = f"""
User query: {query}. 
Relevant source code from the repository:
"""

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    prompt += f"\n\n--- File: {meta['filepath']} ---\n{doc[:1000]}\n"

prompt += """
Based on the 3 code scripts above:
- Explain what needs to be done under the heading Details
- Identify dependencies and risks under the heading Dependencies and Risks
- Suggest Acceptance criteria under the heading Acceptance Criteria
- Suggest test cases under the heading Test Cases
- Provide actionable guidance under the heading Actionable Guidance
- Provide the actual code changes needed to be done
- Only use the supplied source code.
- If insufficient information exists,say so explicitly.
"""

print("Sending to LLM..")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

completion = client.chat.completions.create(
    model="meta/llama-3.3-70b-instruct",
    messages=[{
            "role": "system",
            "content": "You are an experienced Python software architect."
            },
            {
            "role": "user",
            "content": prompt}],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=False
)
print(completion.choices[0].message)


if completion.choices[0].message:
    print("Posting to JIRA")
    jira_story_key = "SCRUM-1"  # Example story ID
    jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_TOKEN))
    issue = jira.issue(jira_story_key)
    issue.update(fields={"description": completion.choices[0].message})
    print(f"LLM output successfully posted to JIRA story {jira_story_key}")
else:
    print("No LLM output available to update JIRA.")
