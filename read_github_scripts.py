import os
from dotenv import load_dotenv
from git import Repo

load_dotenv()

GITHUB_URL = "https://github.com/rajneesh75/python.git"
LOCAL_REPO_PATH = "./my_local_repo"
# How many preview lines to show per file
PREVIEW_LINES = 3


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

                # Print file path
                print("\n==============================")
                print(f"FILE: {full_path}")

                # Read file
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                # Show preview lines
                print("PREVIEW:")
                for line in lines[:PREVIEW_LINES]:
                    print(line.rstrip())

                # Store full file content
                documents.append("".join(lines))
                file_paths.append(full_path)

    print(f"\nFound {len(documents)} Python files")
    return documents, file_paths