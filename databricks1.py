from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()
connection = sql.connect(
    server_hostname=os.getenv("DATABRICKS_HOST"),
    http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_CLUSTER_ID')}",
    access_token=os.getenv("DATABRICKS_TOKEN"))

cursor = connection.cursor()

cursor.execute("SELECT * FROM workspace.gold.customers_policies")
print(cursor.fetchall())

cursor.close()
connection.close()
