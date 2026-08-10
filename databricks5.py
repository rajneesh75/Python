from databricks.connect import DatabricksSession
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)
load_dotenv()

spark = (
    DatabricksSession.builder
    .host("https://dbc-c379cba2-8489.cloud.databricks.com")
    .token(str(os.getenv("DATABRICKS_TOKEN")))
    .serverless(True)
    .getOrCreate()
)
print("Spark Version:", spark.version)

df = spark.read.table("workspace.bronze.products")
df.show()
