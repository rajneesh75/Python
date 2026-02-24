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

# User activity data with high cardinality
user_activity_df = spark.createDataFrame([
                                             ["2024-01-01", f"user_{i}"] for i in range(1, 95001)
                                             # 95,000 distinct users on day 1
                                         ] + [
                                             ["2024-01-02", f"user_{i}"] for i in range(1, 50001)
                                             # 50,000 distinct users on day 2
                                         ], "activity_date: string, user_id: string")

# Quality check: Ensure daily active users don't drop below 60,000
# Using approx_count_distinct is much faster than count_distinct for large datasets
checks = [
    DQDatasetRule(
        criticality="warn",
        check_func=check_funcs.is_aggr_not_less_than,
        column="user_id",
        check_func_kwargs={
            "aggr_type": "approx_count_distinct",  # Fast approximate counting
            "group_by": ["activity_date"],
            "limit": 60000
        },
    ),
]

result_df = dq_engine.apply_checks(user_activity_df, checks)
result_df.show()
