from databricks.connect import DatabricksSession
import logging

logging.basicConfig(level=logging.DEBUG)
spark = DatabricksSession.builder.serverless().getOrCreate()

catalog = "workspace"
schema = "bronze"
table = "Marketing_Engagement"

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv("/Volumes/workspace/bronze/volume1/customers/Marketing_Engagement.csv")
)

print("Schema")
df.printSchema()
print(f"Number of records = {df.count()}")
df.write.mode("overwrite").format("delta").saveAsTable(f"{catalog}.{schema}.{table}")
print("Table created successfully.")
spark.sql(f"SELECT * FROM {catalog}.{schema}.{table} LIMIT 10").show()
