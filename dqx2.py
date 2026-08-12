from databricks.connect import DatabricksSession
from databricks.labs.dqx.config import InputConfig
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.sdk import WorkspaceClient
import logging

logging.basicConfig(level=logging.DEBUG)


spark = DatabricksSession.builder.serverless().getOrCreate()
ws = WorkspaceClient()
profiler = DQProfiler(ws)


# Reading an external table (outside the pipeline)
summary_stats, profiles = profiler.profile_table(
    input_config=InputConfig(location="workspace.bronze.customers")
)

generator = DQGenerator(workspace_client=ws, spark=spark)

checks = generator.generate_dq_rules_ai_assisted(
    user_input="Validate customers data for anomalies and business rules",
    summary_stats=summary_stats
)

print(checks)
print(f"Generated {len(checks)} quality checks from profiler statistics")

# Option B: Without business context (LLM infers rules from statistics alone)
checks = generator.generate_dq_rules_ai_assisted(
    summary_stats=summary_stats
)

print(checks)
print(f"Generated {len(checks)} quality checks from profiler statistics")