from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.sdk import WorkspaceClient
from databricks.connect import DatabricksSession
from databricks.labs.dqx.profiler.profiler import DQProfiler

spark = DatabricksSession.builder.serverless().getOrCreate()


# Initialize the generator
ws = WorkspaceClient()
profiler = DQProfiler(ws)
generator = DQGenerator(ws)
df = spark.read.table("workspace.bronze.customers_cdc1")
profiles = profiler.profile(df)
dataset_profile, column_profiles = profiler.profile(df)
# Step 3: generate rules
checks = generator.generate_dq_rules(column_profiles)
print(checks)
