from databricks.labs.dqx.engine import DQEngine
from databricks.labs.dqx.metrics_observer import DQMetricsObserver
from databricks.labs.dqx import check_funcs
from databricks.labs.dqx.rule import DQRowRule
from databricks.sdk import WorkspaceClient
from databricks.connect import DatabricksSession
from pyspark.sql import functions as F

# Create observer
observer = DQMetricsObserver(name="dq_metrics")
spark = DatabricksSession.builder.serverless().getOrCreate()
df = spark.read.table("workspace.bronze.customers_cdc1")

# Create the engine with the optional observer
engine = DQEngine(WorkspaceClient(), observer=observer)

checks = [
    DQRowRule(
        criticality="error",
        check_func=check_funcs.is_not_null,
        column="customer_id"
    ),
    DQRowRule(
        criticality="error",
        check_func=check_funcs.is_not_null_and_not_empty,
        column=F.trim("customer_name")
    )
]

# Apply checks and get metrics
checked_df, observation = engine.apply_checks(df, checks)

# Trigger an action to populate metrics (e.g., count, save to a table).
# Without triggering an action, metrics will not be populated, and accessing them will result in a stall.
row_count = checked_df.count()

# Access metrics
metrics = observation.get
print(f"Input row count: {metrics['input_row_count']}")
print(f"Error row count: {metrics['error_row_count']}")
print(f"Warning row count: {metrics['warning_row_count']}")
print(f"Valid row count: {metrics['valid_row_count']}")