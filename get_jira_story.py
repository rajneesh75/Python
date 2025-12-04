import os
from dotenv import load_dotenv
import requests
from langchain_core.documents import Document

load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_KEY")
ISSUE_KEY = os.getenv("ISSUE_KEY")


def fetch_issue(issue_key):
    url = f"{JIRA_SERVER}/rest/api/3/issue/{issue_key}"
    response = requests.get(url, auth=(JIRA_EMAIL, JIRA_TOKEN))

    data = response.json()
    summary = data["fields"]["summary"]
    description = data["fields"].get("description", "")

    return summary, description


summary, description = fetch_issue(ISSUE_KEY)

# turn the Jira issue into a document for embeddings
text = f"ISSUE: {ISSUE_KEY}\nSUMMARY: {summary}"
doc = Document(page_content=text)

print(ISSUE_KEY)
print(summary)
