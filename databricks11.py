from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.profiler.dlt_generator import DQDltGenerator
from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient
from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless().getOrCreate()
input_df = spark.read.table("workspace.bronze.customers_cdc1")

# profile input data
ws = WorkspaceClient()
profiler = DQProfiler(ws)
summary_stats, profiles = profiler.profile(input_df)

print(summary_stats)
print()
print(profiles)
print()
# generate DQX quality rules/checks
generator = DQGenerator(ws)

checks = generator.generate_dq_rules(profiles)  # with default level "error"

print(checks)
print()
dq_engine = DQEngine(ws)

# save checks as YAML in arbitrary workspace location
# dq_engine.save_checks(checks, config=WorkspaceFileChecksStorageConfig(location="/Shared/checks1.yml"))

# generate Lakeflow Pipeline (DLT) expectations
dlt_generator = DQDltGenerator(ws)

dlt_expectations = dlt_generator.generate_dlt_rules(profiles, language="SQL")
print(dlt_expectations)
print()
dlt_expectations = dlt_generator.generate_dlt_rules(profiles, language="Python")
print(dlt_expectations)
print()
dlt_expectations = dlt_generator.generate_dlt_rules(profiles, language="Python_Dict")
print(dlt_expectations)
