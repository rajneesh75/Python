from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx import check_funcs
from databricks.labs.dqx.rule import DQRowRule
from databricks.connect import DatabricksSession
from pyspark.sql import functions as F

spark = DatabricksSession.builder.serverless().getOrCreate()
df = spark.read.table("workspace.bronze.customers")
df.printSchema()
df.show(truncate=False)
print(df.columns)

checks = [
    DQRowRule(
        criticality="error",
        check_func=check_funcs.is_not_null,
        column="customer_id"
    ),
    DQRowRule(
        criticality="error",
        check_func=check_funcs.is_not_null_and_not_empty,
        column=F.trim("customer_name")
    )
]

ws = WorkspaceClient()
engine = DQEngine(ws)

results = engine.apply_checks(
    df=df,
    checks=checks
)

results.show(truncate=False)
