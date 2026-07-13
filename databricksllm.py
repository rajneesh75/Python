from databricks.sdk import WorkspaceClient
import logging

logging.basicConfig(level=logging.DEBUG)

ws = WorkspaceClient()

# List all serving endpoints in your workspace
for endpoint in ws.serving_endpoints.list():
    print(endpoint.name, "|", endpoint.state)
