from databricks.connect import DatabricksSession
from databricks.labs.dqx import check_funcs
from databricks.labs.dqx.rule import DQDatasetRule
from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient

default_catalog_name = "main"
default_schema_name = "default"

spark = DatabricksSession.builder.serverless().getOrCreate()

ws = WorkspaceClient()
dq_engine = DQEngine(ws)


# Country data with potential duplicates
country_df = spark.createDataFrame([
    ["US", "USA"],
    ["US", "USA"],  # OK: same code
    ["FR", "FRA"],
    ["FR", "FRN"],  # ERROR: different codes for same country
    ["DE", "DEU"],
], "country: string, country_code: string")

# Quality check: Each country must have exactly one distinct country code
checks = [
    DQDatasetRule(
        criticality="error",
        check_func=check_funcs.is_aggr_not_greater_than,
        column="country_code",
        check_func_kwargs={
            "aggr_type": "count_distinct",  # Exact distinct count per group
            "group_by": ["country"],
            "limit": 1
        },
    ),
]

result_df = dq_engine.apply_checks(country_df, checks)
result_df.show()