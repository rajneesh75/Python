from databricks.labs.dqx.check_funcs import make_condition
from pyspark.sql import functions as F, Column
from databricks.connect import DatabricksSession
from databricks.labs.dqx import check_funcs
from databricks.labs.dqx.check_funcs import sql_expression
import yaml
from databricks.labs.dqx.rule import DQRowRule, DQDatasetRule, register_rule
from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx.config import OutputConfig, InputConfig
from databricks.labs.dqx.check_funcs import is_not_null_and_not_empty

default_catalog_name = "main"
default_schema_name = "default"

spark = DatabricksSession.builder.serverless().getOrCreate()

ws = WorkspaceClient()
dq_engine = DQEngine(ws)

checks = yaml.safe_load("""
- check:
    function: is_not_null
    for_each_column:
    - vendor_id
    - pickup_datetime
    - dropoff_datetime
    - passenger_count
    - trip_distance
    - pickup_longitude
    - pickup_latitude
    - dropoff_longitude
    - dropoff_latitude
  criticality: warn
  filter: total_amount > 0
- check:
    function: is_not_less_than
    arguments:
      column: trip_distance
      limit: 1
  criticality: error
  filter: tip_amount > 0
- check:
    function: sql_expression
    arguments:
      expression: pickup_datetime <= dropoff_datetime
      msg: pickup time must not be greater than dropff time
      name: pickup_datetime_greater_than_dropoff_datetime
  criticality: error
- check:
    function: is_not_in_future
    arguments:
      column: pickup_datetime
  name: pickup_datetime_not_in_future
  criticality: warn
""")

# end-to-end quality checking flow
dq_engine.apply_checks_by_metadata_and_save_in_table(
    input_config=InputConfig("/databricks-datasets/delta-sharing/samples/nyctaxi_2019"),
    checks=checks,
    output_config=OutputConfig(f"{default_catalog_name}.{default_schema_name}.dqx_e2e_output", mode="append"),
    quarantine_config=OutputConfig(f"{default_catalog_name}.{default_schema_name}.dqx_e2e_quarantine", mode="append")
)

# display the results saved to output and quarantine tables
spark.table(f"{default_catalog_name}.{default_schema_name}.dqx_e2e_output").show()
spark.table(f"{default_catalog_name}.{default_schema_name}.dqx_e2e_quarantine").show()

checks = [
    DQDatasetRule(
        criticality="error",
        check_func=check_funcs.foreign_key,
        columns=["col1"],
        check_func_kwargs={
            "ref_columns": ["ref_col1"],
            # either provide reference DataFrame name
            "ref_df_name": "ref_df_key",
            # or provide name of the reference table
            # "ref_table": "catalog1.schema1.ref_table",
        },
    ),
    DQDatasetRule(
        name="foreign_key_check_on_composite_key",
        criticality="warn",
        check_func=check_funcs.foreign_key,
        columns=["col1", "col2"],  # composite key
        check_func_kwargs={
            "ref_columns": ["ref_col1", "ref_col2"],
            "ref_df_name": "ref_df_key",
        },
    ),
]

input_df = spark.createDataFrame([[1, 1], [2, 2], [None, None]], "col1: int, col2: int")
reference_df = spark.createDataFrame([[1, 1]], "ref_col1: int, ref_col2: int")

# When applying foreign key checks with a specified `ref_df_name` argument,
# you must pass a dictionary of reference DataFrame to the `apply_checks` or `apply_checks_and_split` methods
refs_dfs = {"ref_df_key": reference_df}

valid_and_quarantine_df = dq_engine.apply_checks(input_df, checks, ref_dfs=refs_dfs)
valid_and_quarantine_df.show()

# Using yaml to define the foreign key check
checks = yaml.safe_load(
    """
    - criticality: error
      check:
        function: foreign_key
        arguments:
          columns: 
          - col1
          ref_columns: 
          - ref_col1
          # either provide reference DataFrame name
          ref_df_name: ref_df_key
          # or provide name of the reference table
          #ref_table: catalog1.schema1.ref_table
  
    - criticality: warn
      name: foreign_key_check_on_composite_key
      check:
        function: foreign_key
        arguments:
          columns: 
          - col1
          - col2
          ref_columns:
          - ref_col1
          - ref_col2
          ref_df_name: ref_df_key
    """)

input_df = spark.createDataFrame([[1, 1], [2, 2], [None, None]], "col1: int, col2: int")
reference_df = spark.createDataFrame([[1, 1]], "ref_col1: int, ref_col2: int")

# When applying foreign key checks with a specified `ref_df_name` argument,
# you must pass a dictionary of reference DataFrame to the `apply_checks_by_metadata`
# or `apply_checks_by_metadata_and_split` methods
refs_dfs = {"ref_df_key": reference_df}

valid_and_quarantine_df = dq_engine.apply_checks_by_metadata(input_df, checks, ref_dfs=refs_dfs)
valid_and_quarantine_df.show()


@register_rule("row")
def not_ends_with(column: str, suffix: str) -> Column:
    col_expr = F.col(column)
    return make_condition(col_expr.endswith(suffix), f"Column {column} ends with {suffix}",
                          f"{column}_ends_with_{suffix}")


checks = [
    # custom check
    DQRowRule(criticality="warn", check_func=not_ends_with, column="col1", check_func_kwargs={"suffix": "foo"}),
    # sql expression check
    DQRowRule(criticality="warn", check_func=sql_expression, check_func_kwargs={
        "expression": "col1 like 'str%'", "msg": "col1 not starting with 'str'"
    }),
    # built-in check
    DQRowRule(criticality="error", check_func=is_not_null_and_not_empty, column="col1"),
]

schema = "col1: string, col2: string"
input_df = spark.createDataFrame([[None, "foo"], ["foo", None], [None, None]], schema)

valid_and_quarantine_df = dq_engine.apply_checks(input_df, checks)
valid_and_quarantine_df.show()

checks = yaml.safe_load(
    """
    # custom python check
    - criticality: warn
      check:
        function: not_ends_with
        arguments:
          column: col1
          suffix: foo
    # sql expression check
    - criticality: warn
      check:
        function: sql_expression
        arguments:
          expression: col1 like 'str%'
          msg: col1 not starting with 'str'
    # built-in check
    - criticality: error
      check:
        function: is_not_null_and_not_empty
        arguments:
          column: col1
    """
)

schema = "col1: string, col2: string"
input_df = spark.createDataFrame([[None, "foo"], ["foo", None], [None, None]], schema)
custom_check_functions = {"not_ends_with": not_ends_with}
# alternatively, you can also use globals to include all available functions
# custom_check_functions = globals()

status = dq_engine.validate_checks(checks, custom_check_functions)
valid_and_quarantine_df = dq_engine.apply_checks_by_metadata(input_df, checks, custom_check_functions)
valid_and_quarantine_df.show()