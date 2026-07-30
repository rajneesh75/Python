from databricks.sdk import WorkspaceClient
import logging
import os


logging.basicConfig(level=logging.DEBUG)

ws = WorkspaceClient()

# List all serving endpoints in your workspace
for endpoint in ws.serving_endpoints.list():
    print(endpoint.name, "|", endpoint.state)




for k, v in sorted(os.environ.items()):
    if any(x in k.upper() for x in ["MODEL", "LLM", "ENDPOINT", "DATABRICKS"]):
        print(f"{k} = {v}")
