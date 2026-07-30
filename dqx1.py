from databricks.connect import DatabricksSession
from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx.config import InputConfig
import logging

logging.basicConfig(level=logging.DEBUG)
spark = DatabricksSession.builder.serverless().getOrCreate()

ws = WorkspaceClient()
profiler = DQProfiler(ws)

summary_stats, profiles = profiler.profile_table(
    input_config=InputConfig(location="workspace.bronze.customers")
)

print("Summary Statistics:", summary_stats)
print("Generated Profiles:", profiles)