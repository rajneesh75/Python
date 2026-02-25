from databricks.labs.dqx.config import InputConfig, OutputConfig
from databricks.labs.dqx.engine import DQEngine
from databricks.labs.dqx.metrics_observer import DQMetricsObserver
from databricks.labs.dqx import check_funcs
from databricks.labs.dqx.rule import DQRowRule
from databricks.sdk import WorkspaceClient
from databricks.connect import DatabricksSession
from pyspark.sql import functions as F

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

# Create observer
observer = DQMetricsObserver(name="dq_metrics")
spark = DatabricksSession.builder.serverless().getOrCreate()
df = spark.read.table("workspace.bronze.customers_cdc1")

# Create the engine with the optional observer
engine = DQEngine(WorkspaceClient(), observer=observer)

# Create the input config for a batch data source
input_config = InputConfig("workspace.bronze.customers_cdc1")

# Create the output, quarantine, and metrics configs
output_config = OutputConfig("main.default.valid_data")
quarantine_config = OutputConfig("main.default.quarantine_data")  # optional
metrics_config = OutputConfig("main.default.metrics_data")  # optional

# Option 1: Apply checks and save metrics
valid_df, quarantine_df, observation = engine.apply_checks_and_split(df, checks)
quarantine_df.count()  # Trigger an action to populate metrics (e.g. count, save to a table), otherwise accessing
# them will result in a stall

engine.save_summary_metrics(
    observed_metrics=observation.get,
    metrics_config=metrics_config,
    input_config=input_config,  # used as info only
    output_config=output_config,  # used as info only
    quarantine_config=quarantine_config,  # used as info only
    checks_location="checks.yml",  # used as info only
)

# Option 2: Use End to End method: read the data, apply the checks, write data to valid and quarantine tables,
# and write metrics to the metrics table
engine.apply_checks_and_save_in_table(
    checks=checks,
    input_config=input_config,
    output_config=output_config,
    quarantine_config=quarantine_config,
    metrics_config=metrics_config
)

print(observation.get)
