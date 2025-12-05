import os
import requests
from dotenv import load_dotenv

import read_github_scripts
import store_in_chromadb
from find_matching_scripts_to_llm_to_jira import run_semantic_llm_pipeline

load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_KEY")

POLL_JQL = (
    "project = 'Project1' AND "
    "(created >= -800m OR updated >= -800m) "
    "ORDER BY updated DESC"
)

MAX_RESULTS = 50


def validate_env():
    for name in ("JIRA_SERVER", "JIRA_EMAIL", "JIRA_KEY"):
        if not os.getenv(name):
            raise RuntimeError(f"Missing environment variable: {name}")


def read_jira():
    url = f"{JIRA_SERVER}/rest/api/3/search/jql"

    params = {
        "jql": POLL_JQL,
        "fields": "key,summary,created,updated",
        "maxResults": MAX_RESULTS,
    }

    resp = requests.get(url, params=params, auth=(JIRA_EMAIL, JIRA_TOKEN))

    if resp.status_code != 200:
        print("Jira API Error:", resp.text)
        return []

    return resp.json().get("issues", [])


def process_issue(issue):
    key = issue["key"]
    summary = issue["fields"]["summary"]

    print("\n--- Jira Issue ---")
    print("KEY:", key)
    print("SUMMARY:", summary)


def main():
    validate_env()

    print("\nStep 1: Reading GitHub repo...")
    documents, file_paths = read_github_scripts.clone_repository_store_locally()

    print("\nStep 2: Storing Python files in ChromaDB...")
    store_in_chromadb.read_local_repository_store_chromedb(documents, file_paths)

    print("\nStep 3: Reading Jira once...")
    issues = read_jira()

    for issue in issues:
        key = issue["key"]
        summary = issue["fields"]["summary"]
        run_semantic_llm_pipeline(key, summary)

    print("\nDone!")


if __name__ == "__main__":
    main()