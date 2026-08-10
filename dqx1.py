from databricks.connect import DatabricksSession
from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx.config import InputConfig
import logging
import os

logging.basicConfig(level=logging.DEBUG)
spark = (
    DatabricksSession.builder
    .host("https://dbc-c379cba2-8489.cloud.databricks.com")
    .token(os.getenv("DATABRICKS_TOKEN"))
    .serverless(True)
    .getOrCreate()
)
print("Spark Version:", spark.version)

ws = WorkspaceClient()
profiler = DQProfiler(ws)

summary_stats, profiles = profiler.profile_table(
    input_config=InputConfig(location="workspace.bronze.customers")
)

print("Summary Statistics:", summary_stats)
print("Generated Profiles:", profiles)
