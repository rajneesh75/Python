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
spark.sql("USE workspace.bronze")

df = spark.sql(
    "select * from read_files('/Volumes/main/dbdemos_pipeline_bike/raw_data/maintenance_logs/*.csv', format => 'csv') "
    "limit 10")

df.show()
