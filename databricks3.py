from databricks import sql
import os
from dotenv import load_dotenv
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

with sql.connect(
        server_hostname=os.getenv("DATABRICKS_HOST"),
        http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_CLUSTER_ID')}",
        access_token=os.getenv("DATABRICKS_TOKEN")
) as conn:
    print("connection created")
    df = pd.read_sql("SELECT * FROM workspace.bronze.products", conn)

print(df)

