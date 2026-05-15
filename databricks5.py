from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless().getOrCreate()
df = spark.read.table("workspace.gold.customers_policies")
df.show()
