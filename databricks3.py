from databricks import sql
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

with sql.connect(
        server_hostname=os.getenv("DATABRICKS_HOST"),
        http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_CLUSTER_ID')}",
        access_token=os.getenv("DATABRICKS_TOKEN")
) as conn:
    df = pd.read_sql("SELECT * FROM workspace.gold.customers_policies LIMIT 10", conn)

print(df)

