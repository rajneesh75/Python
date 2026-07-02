from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv

load_dotenv()

w = WorkspaceClient()

volume_path = "/Volumes/main/dbdemos_pipeline_bike/raw_data"

for entry in w.dbutils.fs.ls(volume_path):
    print(entry.path)