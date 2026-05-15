from databricks.connect import DatabricksSession
from databricks.labs.dqx.engine import DQEngine
from databricks.labs.dqx.metrics_observer import DQMetricsObserver
from databricks.labs.dqx.config import InputConfig, OutputConfig
from databricks.sdk import WorkspaceClient
from pyspark.sql import Row
import yaml

spark = DatabricksSession.builder.serverless().getOrCreate()

# Define custom metrics
custom_metrics = [
    "sum(array_size(_errors)) as total_check_errors",
    "sum(array_size(_warnings)) as total_check_warnings",
]

# Create the observer with custom metrics
observer = DQMetricsObserver(
    name="business_metrics",
    custom_metrics=custom_metrics
)

# Create the engine with the optional observer
engine = DQEngine(WorkspaceClient(), observer=observer)

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

df = spark.createDataFrame(new_users)

checks = yaml.safe_load("""
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

# Apply checks and get metrics
checked_df, observation = engine.apply_checks_by_metadata(df, checks)

# Trigger an action to populate metrics (e.g., count, save to a table).
# Without triggering an action, metrics will not be populated, and accessing them will result in a stall.
checked_df.count()  # Example action to ensure metrics are computed

# Access metrics
metrics = observation.get
print(f"Input row count: {metrics['input_row_count']}")
print(f"Error row count: {metrics['error_row_count']}")
print(f"Warning row count: {metrics['warning_row_count']}")
print(f"Valid row count: {metrics['valid_row_count']}")
print(f"Total check errors: {metrics['total_check_errors']}")
print(f"Total check warnings: {metrics['total_check_warnings']}")
