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

# Manufacturing sensor data with readings from multiple machines
manufacturing_df = spark.createDataFrame([
    ["M1", "2024-01-01", 20.1],
    ["M1", "2024-01-02", 20.3],
    ["M1", "2024-01-03", 20.2],  # Machine 1: stable readings (low stddev)
    ["M2", "2024-01-01", 18.5],
    ["M2", "2024-01-02", 25.7],
    ["M2", "2024-01-03", 15.2],  # Machine 2: unstable readings (high stddev) - should FAIL
    ["M3", "2024-01-01", 19.8],
    ["M3", "2024-01-02", 20.1],
    ["M3", "2024-01-03", 19.9],  # Machine 3: stable readings
], "machine_id: string, date: string, temperature: double")

# Quality check: Standard deviation should not exceed 3.0 per machine
checks = [
    DQDatasetRule(
        criticality="error",
        check_func=check_funcs.is_aggr_not_greater_than,
        column="temperature",
        check_func_kwargs={
            "aggr_type": "stddev",
            "group_by": ["machine_id"],
            "limit": 3.0
        },
    ),
]

result_df = dq_engine.apply_checks(manufacturing_df, checks)
result_df.show()
