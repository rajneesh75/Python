import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
from jira import JIRA
import logging
from openai import OpenAI

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

LOCAL_REPO_PATH = "./my_local_repo"
COLLECTION_NAME = "python_code_embeddings"

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_KEY")
ISSUE_KEY = os.getenv("ISSUE_KEY")

print("Reading chroma DB...")
chroma_client = chromadb.PersistentClient(path="./my_chroma")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"  # Fast + good for code/text
)

collection = chroma_client.get_collection(name=COLLECTION_NAME, embedding_function=sentence_transformer_ef, )
query = "Modify the script that returns the sum of 2 numbers to instead return a sum of 3 numbers."
results = collection.query(query_texts=[query], n_results=3, include=["documents", "metadatas", "distances"])
print("Possible matching scripts:")
for idx, (doc, meta, score) in enumerate(
        zip(results["documents"][0], results["metadatas"][0], results["distances"][0])):
    print(f"{idx + 1}. File: {meta.get('filepath')}  Score: {score}")
    print(doc[:1000])
    print("-----")

prompt = f"""
Your task is to analyze the user's requested change and modify the supplied source code accordingly.

## User Requirement
User query: {query}. 
## Source Code

The following source code snippets were retrieved from the repository based on semantic search. 
These snippets may belong to one or more files.

"""

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    prompt += f"\n\n--- File: {meta['filepath']} ---\n{doc[:1000]}\n"

prompt += """
## Instructions
1. Analyze all supplied source files.
2. Determine which files require modification to implement the requested change.
3. Modify only the files that actually require changes.
4. Do NOT invent additional files, functions, classes, or APIs that are not present in the supplied source code.
5. If the supplied source code is insufficient to complete the requested change, explicitly state what information is missing.
6. If no changes are required for a file, do not include that file in the output.
7. Produce the response in valid Markdown.
8. Be concise but technically complete.
9. Preserve the existing coding style and architecture where possible.
10. Return complete code only for the functions or code blocks that need modification. Do not rewrite entire files unless necessary.

## Output Format

For every affected file, produce the following sections.

---

# Affected File

**File Name**
`<relative/path/to/file.py>`

## Details

Describe:
- what needs to be changed
- why the change is required
- impact on existing functionality

## Dependencies and Risks

List:
- dependent modules
- impacted functions/classes
- backward compatibility considerations
- potential risks

## Acceptance Criteria

Provide measurable acceptance criteria.

Example:
- Requirement implemented successfully.
- Existing functionality continues to work.
- Unit tests pass.
- No regression introduced.

## Test Cases

Provide test scenarios including:
- Positive tests
- Negative tests
- Edge cases
- Regression tests

## Code Changes

Return only the modified code.

Use fenced Markdown code blocks with the correct language.

Example:

```python
# modified code
```

## Assumptions

List any assumptions made while implementing the change.

---

## Final Summary

At the end of the response include:

- Total affected files
- Files requiring no changes (if any)
- Missing information (if any)
- Overall implementation summary

If the supplied source code is insufficient to safely implement the requested change, clearly explain why and specify 
what additional files or context are needed instead of making assumptions.    
 
"""

with open("prompt.txt", "w") as f:
    f.write(prompt)

print("Sending to LLM..")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

completion = client.chat.completions.create(
    model="meta/llama-3.2-3b-instruct",
    messages=[{
        "role": "system",
        "content": "You are an experienced Python software architect and Senior Developer."
    },
        {
            "role": "user",
            "content": prompt}],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=False
)
response = completion.choices[0].message.content.strip()
print(response)
