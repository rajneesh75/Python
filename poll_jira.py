import os
import time
import requests

from dotenv import load_dotenv

load_dotenv()
JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_KEY")
ISSUE_KEY = os.getenv("ISSUE_KEY")
POLL_JQL = "project = 'Project1' AND (created >= '-20m' OR updated >= '-20m') ORDER BY created DESC"
POLL_INTERVAL = 60

SEEN = set()  # store processed issue IDs


def poll_jira():
    url = f"{JIRA_SERVER}/rest/api/3/search/jql"

    params = {
        "jql": POLL_JQL,
        "fields": "key,summary,updated",
        "maxResults": 50,
    }

    headers = {
        "Accept": "application/json"
    }

    print("sending request")
    response = requests.get(
        url,
        headers=headers,
        params=params,
        auth=(JIRA_EMAIL, JIRA_TOKEN)
    )
    print(response)
    if response.status_code != 200:
        print("Jira API Error:", response.text)
        return []

    body = response.json()
    return body.get("issues", [])


def process_issue(issue):
    key = issue["key"]
    summary = issue["fields"]["summary"]

    print("\n--- New or Updated Issue ---")
    print("KEY:", key)
    print("SUMMARY:", summary)

    # TODO: vector DB embedding here
    # embed_and_store(f"{key}: {summary}")

    SEEN.add(key)


def start_polling():
    print("Starting Jira polling (latest API)...")

    while True:
        try:
            issues = poll_jira()

            for issue in issues:
                if issue["key"] not in SEEN:
                    process_issue(issue)

        except Exception as e:
            print("Polling error:", str(e))

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    start_polling()