from delta.tables import DeltaTable
from databricks.connect import DatabricksSession
from dotenv import load_dotenv
from pyspark.sql import functions as F
import os
import logging

# logging.basicConfig(level=logging.DEBUG)
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
etl_control_version_df = spark.sql("SELECT last_version from etl_control where pipeline = 'product_etl'")
etl_control_version_row = etl_control_version_df.first()

if etl_control_version_row is not None:
    etl_control_version = etl_control_version_row.last_version
else:
    etl_control_version = 0

print(f"etl_control_version {etl_control_version}")

latest_table_version = spark.sql("DESCRIBE HISTORY products").first().version
print(f"table_latest_version {latest_table_version}")

if latest_table_version is not None and latest_table_version > etl_control_version:
    print("New data available")

    read_changes_df = (
        spark.read
        .format("delta")
        .option("readChangeFeed", "true")
        .option("startingVersion", etl_control_version + 1)
        .table("products")
        .filter("_change_type IN ('insert','update_postimage','delete')")
    )

    print("New changes")
    read_changes_df.show()
    try:
        if read_changes_df.head(1):
            print("Running merge")
            target = DeltaTable.forName(spark, "products_warehouse")
            target.alias("t").merge(
                read_changes_df.alias("s"),
                "t.product_id = s.product_id"
            ) \
                .whenMatchedUpdateAll(condition="s._change_type = 'update_postimage'") \
                .whenMatchedDelete(condition="s._change_type = 'delete'") \
                .whenNotMatchedInsertAll() \
                .execute()

        new_etl_version = latest_table_version
        print(f"new_etl_version {new_etl_version}")

        control_tbl = DeltaTable.forName(spark, "etl_control")
        control_tbl.update(condition=f"pipeline = 'product_etl'", set={"last_version": str(new_etl_version)})
    except Exception as e:
        print(f"Pipeline failed: {e}")
        raise
else:
    print("No new data available")

print("current warehouse")
product_warehouse_df = spark.sql("SELECT * FROM products_warehouse order by _commit_timestamp")
product_warehouse_df.show()
