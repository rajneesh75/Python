import os
from dotenv import load_dotenv
from git import Repo

load_dotenv()

GITHUB_URL = "https://github.com/rajneesh75/python.git"
LOCAL_REPO_PATH = "./my_local_repo"


def clone_repository_store_locally():
    # Clone or pull
    if not os.path.exists(LOCAL_REPO_PATH):
        print(f"Cloning {GITHUB_URL}...")
        Repo.clone_from(GITHUB_URL, LOCAL_REPO_PATH)
    else:
        print("Repo already exists locally, pulling latest changes...")
        Repo(LOCAL_REPO_PATH).remotes.origin.pull()

    # Read all Python files
    documents = []
    file_paths = []

    for root, _, files in os.walk(LOCAL_REPO_PATH):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    documents.append(f.read())
                    file_paths.append(full_path)

    print(f"Found {len(documents)} Python files")

    return documents, file_paths