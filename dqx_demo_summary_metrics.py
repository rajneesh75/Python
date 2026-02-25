import yaml
from databricks.connect import DatabricksSession
from databricks.labs.dqx.engine import DQEngine
from databricks.labs.dqx.metrics_observer import DQMetricsObserver
from databricks.sdk import WorkspaceClient
from pyspark.sql import Row
from databricks.labs.dqx.config import OutputConfig
from databricks.labs.dqx.config import InputConfig
import pyspark.sql.functions as F

demo_catalog_name = "main"
demo_schema_name = "default"

spark = DatabricksSession.builder.serverless().getOrCreate()

# `WorkspaceClient` will be authenticated as the current user inside Databricks
ws = WorkspaceClient()
# Create the metrics observer
observer = DQMetricsObserver(name="my_observation")
dq_engine = DQEngine(ws, observer=observer)

checks_from_yaml = yaml.safe_load("""
# 1. Ensure id, age, country are not null or empty (error-level)
- check:
    function: is_not_null_and_not_empty
    for_each_column:  # define check for multiple columns at once
      - id
      - age
      - country
  criticality: error

# 2. Warn if age is outside [18, 120] for Germany or France
- check:
    function: is_in_range
    filter: country in ['Germany', 'France']
    arguments:
      column: age  # define check for a single column
      min_limit: 18
      max_limit: 120
  criticality: warn
  name: age_not_in_range  # optional check name, auto-generated if not provided

# 3. Warn if country is not Germany or France
- check:
    dimension: validity
    function: is_in_list
    for_each_column:
      - country
    arguments:
      allowed:
        - Germany
        - France
  criticality: warn

# 4. Error if id is not unique across the dataset
- check:
    function: is_unique
    arguments:
      columns:
        - id
  criticality: warn
""")

status = DQEngine.validate_checks(checks_from_yaml)
print(f"Checks from YAML: {status}")

# Create the metrics observer
observer = DQMetricsObserver(name="my_observation")  # the name is used as run_name when saving metrics to a table

# Create some input data
new_users = [
    Row(id=1, age=23, country='Germany'),
    Row(id=2, age=30, country='France'),
    Row(id=3, age=16, country='Germany'),  # Invalid -> age - less than 18
    Row(id=None, age=29, country='France'),  # Invalid -> id - NULL
    Row(id=4, age=29, country=''),  # Invalid -> country - Empty
    Row(id=5, age=23, country='Italy'),  # Invalid -> country - not in allowed
    Row(id=6, age=123, country='France'),  # Invalid -> age - greater than 120
    Row(id=2, age=23, country='Germany'),  # duplicated id
]
new_users_df = spark.createDataFrame(new_users)

# Apply the checks and display the row-level results
# Below example uses apply_checks_by_metadata method, but metrics are supported in all apply check methods
validated_df, observation = dq_engine.apply_checks_by_metadata(new_users_df, checks_from_yaml)
validated_df.show()

# Get the summary-level metrics from the returned observation
validated_df.count()
metrics = observation.get
print(metrics)

# Create some input data
new_users = [
    Row(id=1, age=23, country='Germany'),
    Row(id=2, age=30, country='France'),
    Row(id=3, age=16, country='Germany'),  # Invalid -> age - less than 18
    Row(id=None, age=29, country='France'),  # Invalid -> id - NULL
    Row(id=4, age=29, country=''),  # Invalid -> country - Empty
    Row(id=5, age=23, country='Italy'),  # Invalid -> country - not in allowed
    Row(id=6, age=123, country='France'),  # Invalid -> age - greater than 120
    Row(id=2, age=23, country='Germany'),  # duplicated id
]
new_users_df = spark.createDataFrame(new_users)

# Apply the checks
validated_df, observation = dq_engine.apply_checks_by_metadata(new_users_df, checks_from_yaml)

# Setup the output table configuration
output_table_name = f"{demo_catalog_name}.{demo_schema_name}.output_table"
output_config = OutputConfig(location=output_table_name, mode="overwrite")

metrics_table_name = f"{demo_catalog_name}.{demo_schema_name}.metrics_table"
metrics_config = OutputConfig(location=metrics_table_name, mode="overwrite")

# Option 1: Use save metrics method
validated_df.count()  # Trigger an action to populate metrics (e.g. count, save to a table)
dq_engine.save_summary_metrics(observed_metrics=observation.get, metrics_config=metrics_config,
                               output_config=output_config)
# for streaming use a listener (see dqx docs): spark.streams.addListener(get_streaming_metrics_listener(...))

spark.table(metrics_table_name).show()

# Option 2: Use save results method (save metrics and output)
dq_engine.save_results_in_table(
    output_df=validated_df,
    output_config=output_config,
    observation=observation,
    metrics_config=metrics_config
)

spark.table(output_table_name).show()
spark.table(metrics_table_name).show()

# Create some input data
new_users = [
    Row(id=1, age=23, country='Germany'),
    Row(id=2, age=30, country='France'),
    Row(id=3, age=16, country='Germany'),  # Invalid -> age - less than 18
    Row(id=None, age=29, country='France'),  # Invalid -> id - NULL
    Row(id=4, age=29, country=''),  # Invalid -> country - Empty
    Row(id=5, age=23, country='Italy'),  # Invalid -> country - not in allowed
    Row(id=6, age=123, country='France'),  # Invalid -> age - greater than 120
    Row(id=2, age=23, country='Germany'),  # duplicated id
]
new_users_df = spark.createDataFrame(new_users)

# Write the input data to a table
input_table_name = f"{demo_catalog_name}.{demo_schema_name}.input_table"
new_users_df.write.mode("overwrite").saveAsTable(input_table_name)

# Setup the input and output table configuration
input_config = InputConfig(location=input_table_name)

output_table_name = f"{demo_catalog_name}.{demo_schema_name}.output_table"
output_config = OutputConfig(location=output_table_name, mode="overwrite")

metrics_table_name = f"{demo_catalog_name}.{demo_schema_name}.metrics_table"
metrics_config = OutputConfig(location=metrics_table_name, mode="overwrite")

# Read the input data, apply checks, generate metrics, and save results
dq_engine.apply_checks_by_metadata_and_save_in_table(
    checks=checks_from_yaml,
    input_config=input_config,
    output_config=output_config,
    metrics_config=metrics_config
)

spark.table(output_table_name).show()
spark.table(metrics_table_name).show()

# fetch any metrics row as an example
metrics_row = spark.table(metrics_table_name).collect()[0]
run_id = metrics_row["run_id"]
output_table_name = metrics_row["output_location"]

# retrieve detailed results
output_df = spark.table(output_table_name)

# extract errors
results_df = output_df.select(
    F.explode(F.col("_errors")).alias("result"),
).select(F.expr("result.*"))

# extract warnings
results_df = output_df.select(
    F.explode(F.col("_warnings")).alias("result"),
).select(F.expr("result.*"))

results_df.show()

# You can fetch detailed quality results using the run_id from summary metrics
filtered_results_df = results_df.filter(F.col("run_id") == run_id)  # filter, or join
filtered_results_df.show()
