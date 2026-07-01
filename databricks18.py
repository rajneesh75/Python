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

raw_data_volume = "/Volumes/main/dbdemos_pipeline_bike/raw_data/"

# Print out a list of directories in our raw_data volume and a few files from those directories
for table in os.listdir(raw_data_volume):
    print(table + "/")
    for file in os.listdir(raw_data_volume + table)[:3]:
        print("  " + file)
    print("  ...")