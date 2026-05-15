from databricks.connect import DatabricksSession
from databricks.labs.dqx import check_funcs
from databricks.labs.dqx.engine import DQEngine
from databricks.labs.dqx.metrics_observer import DQMetricsObserver
from databricks.labs.dqx.rule import DQRowRule, DQDatasetRule
from databricks.labs.dqx.config import InputConfig, OutputConfig
from databricks.sdk import WorkspaceClient

spark = DatabricksSession.builder.serverless().getOrCreate()

# Define the checks
checks = [
    DQRowRule(
        criticality="warn",
        check_func=check_funcs.is_not_null,
        column="mobile",
    ),
    DQDatasetRule(
        criticality="error",
        check_func=check_funcs.is_unique,
        columns=["customer_id", "customer_name"],
    ),
    DQRowRule(
        name="email_invalid_format",
        criticality="error",
        check_func=check_funcs.regex_match,
        column="email",
        check_func_kwargs={"regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"},
    ),
]

# Create the observer
observer = DQMetricsObserver(name="dq_metrics")

# Create the engine with the metrics observer
engine = DQEngine(WorkspaceClient(), observer=observer)

# Create the input config for a streaming data source
input_config = InputConfig("workspace.bronze.customers_cdc", is_streaming=True)

# Create the output, quarantine, and metrics configs
output_config = OutputConfig(
    location="main.default.valid_data",
    trigger={"availableNow": True},  # stop the stream once all data is processed
    # use a Volume in production for persistence
    options={"checkpointLocation": "/Workspace/Users/rajneesh75@gmail.com/checkpoints/valid_data"}
)
quarantine_config = OutputConfig(
    location="main.default.quarantine_data",
    trigger={"availableNow": True},  # stop the stream once all data is processed
    options={"checkpointLocation": "/Workspace/Users/rajneesh75@gmail.com/checkpoints/quarantine_data"}
)
metrics_config = OutputConfig("main.default.metrics_data")  # streaming configuration not required for metrics

# Option 1: Apply checks and save metrics
df = spark.readStream.table(input_config.location)
valid_df, quarantine_df, observation = engine.apply_checks_and_split(df, checks)
output_query = valid_df.writeStream.format(output_config.format).outputMode(output_config.mode).options(
    **output_config.options).trigger(**output_config.trigger).toTable(output_config.location)
quarantine_query = quarantine_df.writeStream.format(quarantine_config.format).outputMode(
    quarantine_config.mode).options(**quarantine_config.options).trigger(**quarantine_config.trigger).toTable(
    quarantine_config.location)

listener = engine.get_streaming_metrics_listener(
    input_config=input_config,
    output_config=output_config,
    quarantine_config=quarantine_config,
    metrics_config=metrics_config,
    target_query_id=quarantine_query.id,
)
# for streaming writing metrics requires a stream listener, observation cannot be accessed directly
# this adds a global listener for the current Spark session so do not add it again if reusing the same session
spark.streams.addListener(listener)

output_query.awaitTermination()
quarantine_query.awaitTermination()

# Option 2: Use End-to-End method: read the data, apply the checks, write data to valid and quarantine tables,
# and write metrics to the metrics table
# Output and quarantine data will be written in streaming and summary metrics will be written for each micro-batch
engine.apply_checks_and_save_in_table(
    checks=checks,
    input_config=input_config,
    output_config=output_config,
    quarantine_config=quarantine_config,
    metrics_config=metrics_config
)
