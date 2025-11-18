import subprocess
import base64
import json
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

# Check if the file already exists (to get SHA for updates)
check_cmd = f'curl -H "Authorization: token {GITHUB_TOKEN}" {UPLOAD_URL}'
check_result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
print(check_result.stdout)
response_json = json.loads(check_result.stdout or "{}")

sha = response_json.get("sha")  # Get file SHA if it exists

# Read file content and encode it in base64
with open(FILE_PATH, "rb") as file:
    content = base64.b64encode(file.read()).decode().replace("\n", "")

# Prepare request payload
payload = {
    "message": "upload",
    "content": content,
    "branch": BRANCH
}
print(payload)

if sha:
    payload["sha"] = sha  # Required for updating an existing file
# cURL command to upload the file
curl_cmd = f'curl -X PUT -H "Authorization: token {GITHUB_TOKEN}" -H "Content-Type: application/text" -d \"{json.dumps(payload)}\" {UPLOAD_URL}'

# Run the cURL command
result = subprocess.run(curl_cmd, capture_output=True, text=True)
print(result.returncode)
print(result.stdout)
print(result.stderr)
