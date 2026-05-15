from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# List all serving endpoints in your workspace
for endpoint in w.serving_endpoints.list():
    print(endpoint.name, "|", endpoint.state)