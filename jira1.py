from jira import JIRA
import os
from dotenv import load_dotenv

load_dotenv()
print("Loaded:", os.getenv("JIRA_KEY"))

# --- CONFIGURE THESE ---
JIRA_SERVER = "https://rajneesh75.atlassian.net"
JIRA_EMAIL = "rajneesh75@gmail.com"
JIRA_TOKEN = os.getenv("JIRA_KEY")
ISSUE_KEY = "SCRUM-1"   # e.g. story/bug number

# --- CONNECT ---
jira = JIRA(
    server=JIRA_SERVER,
    basic_auth=(JIRA_EMAIL, JIRA_TOKEN),
)

# --- GET ISSUE ---
issue = jira.issue(ISSUE_KEY)
print(issue)

# --- PRINT SUMMARY (User Story Title) ---
print("User Story Name:", issue.fields.summary)