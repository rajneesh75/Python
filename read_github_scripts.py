import os
from dotenv import load_dotenv
from git import Repo


load_dotenv()

# Replace with your GitHub Personal Access Token (PAT)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
FILE_PATH = os.getenv("FILE_PATH")  # Local file path
GITHUB_FILE_PATH = os.getenv("GITHUB_FILE_PATH")  # Path in the repo
BRANCH = os.getenv("BRANCH")  # Change if needed

# ---------------------------
# CONFIGURATION
# ---------------------------
GITHUB_URL = "https://github.com/rajneesh75/python.git"
LOCAL_REPO_PATH = "./my_local_repo"
COLLECTION_NAME = "python_code_embeddings"

# ---------------------------
# STEP 1 — Clone repository
# ---------------------------
if not os.path.exists(LOCAL_REPO_PATH):
    print(f"Cloning {GITHUB_URL}...")
    Repo.clone_from(GITHUB_URL, LOCAL_REPO_PATH)
else:
    print("Repo already exists locally, skipping clone")
    repo = Repo(LOCAL_REPO_PATH)
    print("Pulling latest changes from remote...")
    repo.remotes.origin.pull()

# ---------------------------
# STEP 2 — Load all Python files recursively
# ---------------------------
documents = []
file_paths = []

for root, dirs, files in os.walk(LOCAL_REPO_PATH):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                print(path)
                print(content)
                documents.append(content)
                file_paths.append(path)
                print('-----------------')

print(f"Found {len(documents)} Python files")

