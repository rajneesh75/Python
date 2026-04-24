from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.engine import DQEngine
from databricks.labs.dqx.config import WorkspaceFileChecksStorageConfig, TableChecksStorageConfig

spark = DatabricksSession.builder.serverless().getOrCreate()

catalog = "workspace"
schema = "bronze"

workspace_client = WorkspaceClient()
profiler = DQProfiler(workspace_client=workspace_client, spark=spark)
results = profiler.profile_tables_for_patterns(
    patterns=[f"{catalog}.{schema}.customers", f"{catalog}.{schema}.orders"],
)

# Process results for each table
for table, (summary_stats, profiles) in results.items():
    print(f"Table: {table}")
    print(f"Table statistics: {summary_stats}")
    print(f"Generated profiles: {profiles}")
