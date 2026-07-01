from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

ws = WorkspaceClient()


def list_workspace_all(path="/"):
    for obj in ws.workspace.list(path):
        obj_type = obj.object_type.name if obj.object_type else "UNKNOWN"
        print(f"{obj_type:10} {obj.path}")

        if obj.object_type and obj.object_type.name == "DIRECTORY":
            list_workspace_all(obj.path)


list_workspace_all("/")
