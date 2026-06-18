from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.profiler.dlt_generator import DQDltGenerator
from databricks.labs.dqx.config import FileChecksStorageConfig
from databricks.labs.dqx.engine import DQEngine
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient

spark = DatabricksSession.builder.serverless().getOrCreate()
input_df = spark.read.table("workspace.bronze.customers_cdc")

# profile input data
ws = WorkspaceClient()
profiler = DQProfiler(ws)

summary_stats, profiles = profiler.profile(input_df)
print(summary_stats)
print(profiles)

# generate DQX quality rules/checks
generator = DQGenerator(ws)
checks = generator.generate_dq_rules(profiles)  # with default level "error"

dq_engine = DQEngine(ws)

# save checks as YAML in arbitrary workspace location
# dq_engine.save_checks(checks, config=WorkspaceFileChecksStorageConfig(location="/Users/rajneesh75@gmail.com/databricks/checks.yml"))

dq_engine.save_checks(checks, config=FileChecksStorageConfig(location="checks_customers_cdc.yml"))
print("Checks saved")

# generate Lakeflow Pipeline (DLT) expectations
dlt_generator = DQDltGenerator(ws)

dlt_expectations = dlt_generator.generate_dlt_rules(profiles, language="SQL")
print(dlt_expectations)

dlt_expectations = dlt_generator.generate_dlt_rules(profiles, language="Python")
print(dlt_expectations)

dlt_expectations = dlt_generator.generate_dlt_rules(profiles, language="Python_Dict")
print(dlt_expectations)
