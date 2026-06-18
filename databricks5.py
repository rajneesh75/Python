from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless().getOrCreate()
print("connection created")
df = spark.read.table("workspace.bronze.products")
df.show()
