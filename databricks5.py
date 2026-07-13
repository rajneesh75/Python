from databricks.connect import DatabricksSession
import logging

logging.basicConfig(level=logging.DEBUG)
spark = DatabricksSession.builder.serverless().getOrCreate()
print("connection created")
df = spark.read.table("workspace.bronze.products")
df.show()
