from databricks.sdk import WorkspaceClient

ws = WorkspaceClient()


def list_workspace_all(path="/"):
    for obj in ws.workspace.list(path):
        # Print the item (folder / notebook / file)
        print(f"{obj.object_type.name:10}  {obj.path}")

        # If it's a folder, go inside it
        if obj.object_type.name == "DIRECTORY":
            list_workspace_all(obj.path)


list_workspace_all("/")
