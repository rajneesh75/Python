from databricks.connect import DatabricksSession
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

spark = (
    DatabricksSession.builder
    .host("https://dbc-c379cba2-8489.cloud.databricks.com")
    .token(str(os.getenv("DATABRICKS_TOKEN")))
    .serverless(True)
    .getOrCreate()
)
print("Spark Version:", spark.version)
spark.sql("USE main.dbdemos_ai_agent")

df = spark.sql("SELECT * FROM get_customer_by_email('john21@example.net')")

df.show()
