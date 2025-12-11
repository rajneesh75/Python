import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import requests
import os
from jira import JIRA

load_dotenv()

LOCAL_REPO_PATH = "./my_local_repo"
COLLECTION_NAME = "python_code_embeddings"

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_KEY")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

NO_OF_MATCHES = 5


def run_semantic_llm_pipeline(issue_key, issue_summary):
    print(f"\nRunning semantic match in inmemory ChromaDB for Jira issue:- {issue_key} and {issue_summary}")

    client = chromadb.Client()
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"  # Fast + good for code/text
    )

    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=sentence_transformer_ef,)

    # Use the JIRA issue summary as the query
    # TOP n scripts
    results = collection.query(query_texts=[issue_summary], n_results=NO_OF_MATCHES)

    print("\nPossible matching scripts from most matching(Least distance) to least matching(Most distance:")
    for idx, (doc, meta, score) in enumerate(
            zip(results["documents"][0], results["metadatas"][0], results["distances"][0])):
        print(f"{idx + 1}. File: {meta.get('filepath')}  Score: {score}")
        print(doc[:600])
        print("-----")

    print("Sending to LLM...")

    # ---- Build LLM Prompt ----
    prompt = f"""You are an expert in Python. For Jira Issue {issue_key} with summary: {issue_summary}.
            Below Relevant source code/s from the repository:"""

    for idx, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        prompt += f"\n{idx + 1}. File: {meta['filepath']} ---\n{doc[:700]}\n"

    prompt += """  
        You are an expert software engineer  
        Based on the code scripts above:
        - Mention on top which code script you are talking about under the heading Code Script Reference
        - Explain what needs to be done under the heading Details
        - Identify dependencies and risks under the heading Dependencies and Risks
        - Suggest Acceptance criteria under the heading Acceptance Criteria
        - Suggest test cases under the heading Test Cases
        - Provide actionable guidance under the heading Actionable Guidance
        - Provide the actual code changes needed to be done"""

    print(prompt)
    print("\nSending to LLM")

    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    stream = False

    headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Accept": "application/json",
               "Content-Type": "application/json", }

    payload = {
        "model": "meta/llama-4-maverick-17b-128e-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 1.00,
        "top_p": 1.00,
        "frequency_penalty": 0.00,
        "presence_penalty": 0.00,
        "stream": stream
    }

    response = requests.post(invoke_url, headers=headers, json=payload)
    json_resp = response.json()
    llm_output = json_resp["choices"][0]["message"]["content"]
    print("\nLLM OUTPUT:")
    print(llm_output)

    print("\nPosting to JIRA...")

    jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_TOKEN))
    issue = jira.issue(issue_key)
    issue.update(fields={"description": llm_output})
    print(f"\nLLM output successfully posted to JIRA issue {issue_key}")

    return llm_output
