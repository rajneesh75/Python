import os
from dotenv import load_dotenv
import requests

load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_KEY")
ISSUE_KEY = os.getenv("ISSUE_KEY")


def fetch_issue(issue_key):
    url = f"{JIRA_SERVER}/rest/api/3/issue/{issue_key}"
    response = requests.get(url, auth=(JIRA_EMAIL, JIRA_TOKEN))
    if response.status_code != 200:
        print("Failed to fetch issue:", response.text)
        return None
    data = response.json()
    summary = data["fields"]["summary"]

    return summary


summary = fetch_issue(ISSUE_KEY)

# turn the Jira issue into a document for embeddings
text = f"ISSUE: {ISSUE_KEY}\nSUMMARY: {summary}"
print(ISSUE_KEY)
print(summary)
