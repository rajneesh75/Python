from databricks.connect import DatabricksSession
from databricks.labs.dqx import check_funcs
from databricks.labs.dqx.engine import DQEngine
from databricks.labs.dqx.metrics_observer import DQMetricsObserver
from databricks.labs.dqx.rule import DQRowRule, DQDatasetRule
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx.config import OutputConfig
from databricks.labs.dqx.config import InputConfig

demo_catalog_name = "main"
demo_schema_name = "default"

spark = DatabricksSession.builder.serverless().getOrCreate()

# `WorkspaceClient` will be authenticated as the current user inside Databricks
ws = WorkspaceClient()
# Create the metrics observer
observer = DQMetricsObserver(name="my_observation")
df = spark.read.table("workspace.bronze.customers_cdc")

# Create the engine with the metrics observer
engine = DQEngine(WorkspaceClient(), observer=observer)

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

# Create the input config for a batch data source
input_config = InputConfig("workspace.bronze.customers_cdc")

# Create the output, quarantine, and metrics configs
output_config = OutputConfig("main.default.valid_data")
quarantine_config = OutputConfig("main.default.quarantine_data")  # optional
metrics_config = OutputConfig("main.default.metrics_data")  # optional

# Option 1: Apply checks and save metrics
valid_df, quarantine_df, observation = engine.apply_checks_and_split(df, checks)

# Trigger an action to populate metrics (e.g. count, save to a table),
# otherwise accessing them will result in a stall
quarantine_df.count()

engine.save_summary_metrics(
    observed_metrics=observation.get,
    metrics_config=metrics_config,
    input_config=input_config,  # used as info only
    output_config=output_config,  # used as info only
    quarantine_config=quarantine_config,  # used as info only
    checks_location="checks_customers.yml",  # used as info only
)

# Option 2: Use End to End method: read the data, apply the checks,
# write data to valid and quarantine tables, and write metrics to the metrics table
engine.apply_checks_and_save_in_table(
    checks=checks,
    input_config=input_config,
    output_config=output_config,
    quarantine_config=quarantine_config,
    metrics_config=metrics_config
)
