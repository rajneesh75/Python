from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.profiler.dlt_generator import DQDltGenerator

from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient
from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless().getOrCreate()
input_df = spark.read.table("workspace.gold.customers_policies")

# profile input data
ws = WorkspaceClient()
print(ws)

profiler = DQProfiler(ws)
summary_stats, profiles = profiler.profile(input_df)

# generate DQX quality rules/checks
generator = DQGenerator(ws)
checks = generator.generate_dq_rules(profiles)  # with default level "error"

dq_engine = DQEngine(ws)
print(dq_engine)

# generate Lakeflow Pipeline (DLT) expectations
dlt_generator = DQDltGenerator(ws)

dlt_expectations = dlt_generator.generate_dlt_rules(profiles, language="SQL")
print(dlt_expectations)

dlt_expectations = dlt_generator.generate_dlt_rules(profiles, language="Python")
print(dlt_expectations)
