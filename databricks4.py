import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

server_hostname = os.getenv("DATABRICKS_HOST")
http_path = f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_CLUSTER_ID')}"
access_token = os.getenv("DATABRICKS_TOKEN")

engine = create_engine(
    f"databricks://token:{access_token}@{server_hostname}?http_path={http_path}"
)
df = pd.read_sql("SELECT * FROM workspace.gold.customers_policies", engine)

print(df)
