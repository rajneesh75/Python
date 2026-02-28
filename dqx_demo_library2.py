from databricks.labs.dqx.check_funcs import make_condition
from pyspark.sql import functions as F, Column
from databricks.connect import DatabricksSession
from databricks.labs.dqx import check_funcs
from databricks.labs.dqx.check_funcs import sql_expression
import yaml
from databricks.labs.dqx.rule import DQRowRule, DQDatasetRule, register_rule
from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx.config import OutputConfig, InputConfig
from databricks.labs.dqx.check_funcs import is_not_null_and_not_empty

default_catalog_name = "main"
default_schema_name = "default"

spark = DatabricksSession.builder.serverless().getOrCreate()

ws = WorkspaceClient()
dq_engine = DQEngine(ws)

# read the data, limit to 1000 rows for demo purpose
bronze_df = spark.read.format("delta").load("/databricks-datasets/delta-sharing/samples/nyctaxi_2019").limit(1000)
bronze_df.show()
# apply your business logic here
bronze_transformed_df = bronze_df.filter("vendor_id in (1, 2)")

checks = yaml.safe_load("""
- check:
    function: is_not_null
    for_each_column:
    - vendor_id
    - pickup_datetime
    - dropoff_datetime
    - passenger_count
    - trip_distance
    - pickup_longitude
    - pickup_latitude
    - dropoff_longitude
    - dropoff_latitude
  criticality: warn
  filter: total_amount > 0
- check:
    function: is_not_less_than
    arguments:
      column: trip_distance
      limit: 1
  criticality: error
  filter: tip_amount > 0
- check:
    function: sql_expression
    arguments:
      expression: pickup_datetime <= dropoff_datetime
      msg: pickup time must not be greater than dropff time
      name: pickup_datetime_greater_than_dropoff_datetime
  criticality: error
- check:
    function: is_not_in_future
    arguments:
      column: pickup_datetime
  name: pickup_datetime_not_in_future
  criticality: warn
""")

# apply quality checks
silver_df, quarantine_df = dq_engine.apply_checks_by_metadata_and_split(bronze_transformed_df, checks)

# save results
dq_engine.save_results_in_table(
    output_df=silver_df,
    quarantine_df=quarantine_df,
    output_config=OutputConfig(f"{default_catalog_name}.{default_schema_name}.dqx_output", mode="append"),
    quarantine_config=OutputConfig(f"{default_catalog_name}.{default_schema_name}.dqx_quarantine", mode="append")
)

spark.table(f"{default_catalog_name}.{default_schema_name}.dqx_output").show()
spark.table(f"{default_catalog_name}.{default_schema_name}.dqx_quarantine").show()



