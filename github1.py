import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()


# Replace with your GitHub Personal Access Token (PAT)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
FILE_PATH = os.getenv("FILE_PATH")  # Local file path
GITHUB_FILE_PATH = os.getenv("GITHUB_FILE_PATH")  # Path in the repo
BRANCH = os.getenv("BRANCH")  # Change if needed

# GitHub API URL for file upload
UPLOAD_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{GITHUB_FILE_PATH}"

proxies = {
    "http": None,
    "https": None
}

# Read file content and encode it in base64
with open(FILE_PATH, "rb") as file:
    content = base64.b64encode(file.read()).decode()

# Prepare request payload
payload = {
    "message": "Adding file via API",
    "content": content,
    "branch": BRANCH
}

# Set headers
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Send request
response = requests.put(UPLOAD_URL, json=payload, headers=headers, proxies=proxies)

# Check response
if response.status_code == 201:
    print("✅ Successfully connected to GitHub!")
    print("User Info:", response.json())
    print(response.headers)

else:
    print("❌ Failed to connect:", response.status_code, response.text)
