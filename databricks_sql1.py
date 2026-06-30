from delta.tables import DeltaTable
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

bronze_orders_df = spark.sql("select * from workspace.bronze.orders")
bronze_orders_df.show()

silver_orders_df = spark.sql("select * from workspace.silver.orders")
silver_orders_df.show()

gold_orders_df = spark.sql("select * from workspace.gold.gold_sales")
gold_orders_df.show()
