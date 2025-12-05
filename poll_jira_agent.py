from typing import TypedDict, Optional
import os
import time
import requests
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_KEY")
ISSUE_KEY = os.getenv("ISSUE_KEY")
POLL_JQL = "project = 'Project1' AND created >= -15m ORDER BY created DESC"
POLL_INTERVAL = 60


def jira_search(jql):
    """Search JIRA issues using JQL"""
    url = f"{JIRA_SERVER}/rest/api/3/search/jql"
    payload = {
        "queries": [
            {
                "jql": jql,
                "startAt": 0,
                "maxResults": 20,
                "fields": ["key", "summary", "description"]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    resp = requests.post(
        url,
        json=payload,
        headers=headers,
        auth=(JIRA_EMAIL, JIRA_TOKEN),
        timeout=15
    )

    if resp.status_code != 200:
        print("JIRA search failed:", resp.text)
        return []

    data = resp.json()
    print(data)

    # Jira returns results inside "queries" → "results"
    try:
        return data["queries"][0]["results"]
    except:
        return []


# 1) Define the state schema for ingestion
class IngestState(TypedDict, total=False):
    jira_key: str  # input (required when invoking)
    story_summary: str  # filled by node
    error: str  # populated on failure


# 2) Jira fetch function (node)
def fetch_issue_node(state: IngestState) -> IngestState:
    """
    Node: given state with jira_key, fetch summary from JIRA.
    Returns dict with story_summary (or error).
    """
    issue_key = state.get("jira_key")
    if not issue_key:
        return {"error": "missing jira_key in state"}

    try:
        url = f"{JIRA_SERVER}/rest/api/3/issue/{issue_key}"
        resp = requests.get(url, auth=(JIRA_EMAIL, JIRA_TOKEN), timeout=15)

        if resp.status_code != 200:
            return {"error": f"JIRA fetch failed: {resp.status_code} {resp.text}"}

        data = resp.json()
        fields = data.get("fields", {})

        # jiras often have complex description types; this keeps it simple
        summary = fields.get("summary")

        return {"story_summary": summary}

    except Exception as e:
        return {"error": f"exception while fetching jira: {str(e)}"}


# 3) Build the graph that only has the ingest node (for now)
workflow = StateGraph(IngestState)
workflow.add_node("ingest", fetch_issue_node)
workflow.set_entry_point("ingest")
workflow.add_edge("ingest", END)
agent = workflow.compile()


# -----------------------------------------------------
# POLLING LOOP: AUTOMATICALLY CHECK NEW STORIES
# -----------------------------------------------------
def poll_loop():
    print("🚀 Starting JIRA polling...\n")

    seen = set()  # store issue keys already processed

    while True:
        print("🔍 Checking for new issues...")

        # Example JQL: newest issues
        issues = jira_search(POLL_JQL)

        for issue in issues:
            key = issue["key"]

            if key not in seen:
                print(f"\n📌 New issue detected: {key}")

                result = agent.invoke({"jira_key": key})

                if result.get("error"):
                    print(f"❌ Error fetching {key}: {result['error']}")
                else:
                    print(f"✅ Summary for {key}: {result['story_summary']}")

                seen.add(key)

        print(f"⏳ Sleeping for {POLL_INTERVAL} seconds...\n")
        time.sleep(POLL_INTERVAL)


# -----------------------------------------------------
# RUNNING THE POLLER
# -----------------------------------------------------
if __name__ == "__main__":
    poll_loop()
