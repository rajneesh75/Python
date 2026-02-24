from pyspark.sql import functions as F
from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.profiler.dlt_generator import DQDltGenerator
from databricks.connect import DatabricksSession
from databricks.labs.dqx import check_funcs
import yaml
from databricks.labs.dqx.rule import DQRowRule, DQDatasetRule, DQForEachColRule
from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx.config import TableChecksStorageConfig

default_catalog_name = "main"
default_schema_name = "default"

schema = "col1: int, col2: int, col3: int, col4 int"

spark = DatabricksSession.builder.serverless().getOrCreate()
input_df = spark.createDataFrame([[1, 3, 3, 1], [2, None, 4, 1]], schema)

ws = WorkspaceClient()
dq_engine = DQEngine(ws)

# profile the input data
profiler = DQProfiler(ws)
# change the default sample fraction from 30% to 100% for demo purpose
summary_stats, profiles = profiler.profile(input_df, options={"sample_fraction": 1.0})
print(yaml.safe_dump(summary_stats))
print(profiles)

# generate DQX quality rules/checks candidates.they should be manually reviewed before being applied to the data
generator = DQGenerator(ws)
checks = generator.generate_dq_rules(profiles)  # with default level "error"
print(yaml.safe_dump(checks))
yaml.safe_dump(checks, open("dqx_demo_checks.yml", "w"))

# save generated checks in a Delta table
dq_engine.save_checks(
    checks=checks,
    config=TableChecksStorageConfig(location=f"{default_catalog_name}.{default_schema_name}.dqx_checks_table",
                                    mode="overwrite")
)

# generate Lakeflow Pipeline (formerly Delta Live Table (DLT)) expectations
dlt_generator = DQDltGenerator(ws)

dlt_expectations = dlt_generator.generate_dlt_rules(profiles, language="SQL")
print(dlt_expectations)

dlt_expectations = dlt_generator.generate_dlt_rules(profiles, language="Python")
print(dlt_expectations)

dlt_expectations = dlt_generator.generate_dlt_rules(profiles, language="Python_Dict")
print(dlt_expectations)

input_df = spark.createDataFrame([[1, 3, 3, 2], [3, 3, None, 1]], schema)

# load check from file
with open('dqx_demo_checks.yml', "r") as f:
    checks = yaml.safe_load(f)

# Option 1: apply quality rules and quarantine invalid records
valid_df, quarantine_df = dq_engine.apply_checks_by_metadata_and_split(input_df, checks)
valid_df.show()
quarantine_df.show()

# Option 2: apply quality rules and annotate invalid records as additional columns (`_warning` and `_error`)
valid_and_quarantine_df = dq_engine.apply_checks_by_metadata(input_df, checks)
valid_and_quarantine_df.show()

input_df = spark.createDataFrame([[1, 3, 3, 2], [3, 3, None, 1]], schema)

# load checks from a Delta table
dq_engine = DQEngine(WorkspaceClient())
checks = dq_engine.load_checks(
    config=TableChecksStorageConfig(location=f"{default_catalog_name}.{default_schema_name}.dqx_checks_table"))

# Option 1: apply quality rules and quarantine invalid records
valid_df, quarantine_df = dq_engine.apply_checks_by_metadata_and_split(input_df, checks)
valid_df.show()
quarantine_df.show()

# Option 2: apply quality rules and annotate invalid records as additional columns (`_warning` and `_error`)
valid_and_quarantine_df = dq_engine.apply_checks_by_metadata(input_df, checks)
valid_and_quarantine_df.show()

checks = yaml.safe_load("""
- criticality: invalid_criticality
  check:
    function: is_not_null
    for_each_column:
    - col1
    - col2
""")

status = dq_engine.validate_checks(checks)
print(status.has_errors)
print(status.errors)

checks = yaml.safe_load("""
# check for a single column
- criticality: warn
  check:
    function: is_not_null_and_not_empty
    arguments:
      column: col3
# check for multiple column
- criticality: error
  check:
    function: is_not_null
    for_each_column:
    - col1
    - col2
# check with a filter
- criticality: warn
  filter: col1 < 3
  check:
    function: is_not_null_and_not_empty
    arguments:
      column: col4
# check with user metadata
- criticality: warn
  check:
    function: is_not_null_and_not_empty
    arguments:
      column: col5
  user_metadata:
    check_category: completeness
    responsible_data_steward: someone@email.com
# check with auto-generated name
- criticality: warn
  check:
    function: is_in_list
    arguments:
      column: col1
      allowed:
        - 1
        - 2
# check for a struct field
- check:
    function: is_not_null
    arguments:
      column: col7.field1
  # "error" criticality used if not provided
# check for a map element
- criticality: error
  check:
    function: is_not_null
    arguments:
      column: try_element_at(col5, 'key1')
# check for an array element
- criticality: error
  check:
    function: is_not_null
    arguments:
      column: try_element_at(col6, 1)
# check uniqueness of composite key, multi-column rule   
- criticality: error
  check:
    function: is_unique
    arguments:
      columns:
      - col1
      - col2
- criticality: error
  check:
    function: is_aggr_not_greater_than
    arguments:
      column: col1
      aggr_type: count
      limit: 10
- criticality: error
  check:
    function: is_aggr_not_less_than
    arguments:
      column: col1
      aggr_type: count
      limit: 1.2
""")

# validate the checks
status = DQEngine.validate_checks(checks)
assert not status.has_errors

schema = ("col1: int, col2: int, col3: int, col4 int, col5: map<string, string>,"
          " col6: array<string>, col7: struct<field1: int>")
input_df = spark.createDataFrame([
    [1, 3, 3, None, {"key1": ""}, [""], {"field1": 1}],
    [3, None, 4, 1, {"key1": None}, [None], {"field1": None}],
    [None, None, None, None, None, None, None],
], schema)

# Option 1: apply quality rules and quarantine invalid records
valid_df, quarantine_df = dq_engine.apply_checks_by_metadata_and_split(input_df, checks)
valid_df.show()
quarantine_df.show()

# Option 2: apply quality rules and annotate invalid records as additional columns (`_warning` and `_error`)
valid_and_quarantine_df = dq_engine.apply_checks_by_metadata(input_df, checks)
valid_and_quarantine_df.show()

checks = [
    DQRowRule(  # check for a single column
        name="col3_is_null_or_empty",
        criticality="warn",
        check_func=check_funcs.is_not_null_and_not_empty,
        column="col3"
    ),
    *DQForEachColRule(  # check for multiple columns
        columns=["col1", "col2"],
        criticality="error",
        check_func=check_funcs.is_not_null).get_rules(),
    DQRowRule(  # check with a filter
        name="col_4_is_null_or_empty",
        criticality="warn",
        filter="col1 < 3",
        check_func=check_funcs.is_not_null_and_not_empty,
        column="col4"
    ),
    DQRowRule(
        criticality="warn",
        check_func=check_funcs.is_not_null_and_not_empty,
        column='col3',
        user_metadata={
            "check_type": "completeness",
            "responsible_data_steward": "someone@email.com"
        }
    ),
    DQRowRule(  # provide check func arguments using positional arguments
        criticality="warn",
        check_func=check_funcs.is_in_list,
        column="col1",
        check_func_args=[[1, 2]]
    ),
    DQRowRule(  # provide check func arguments using keyword arguments
        criticality="warn",
        check_func=check_funcs.is_in_list,
        column="col2",
        check_func_kwargs={"allowed": [1, 2]}
    ),
    DQRowRule(  # check for a struct field
        # "error" criticality used if not provided
        check_func=check_funcs.is_not_null,
        column="col7.field1"
    ),
    DQRowRule(  # check for a map element
        criticality="error",
        check_func=check_funcs.is_not_null,
        column=F.try_element_at("col5", F.lit("key1"))
    ),
    DQRowRule(  # check for an array element
        criticality="error",
        check_func=check_funcs.is_not_null,
        column=F.try_element_at("col6", F.lit(1))
    ),
    DQDatasetRule(  # check uniqueness of composite key, multi-column rule
        criticality="error",
        check_func=check_funcs.is_unique,
        columns=["col1", "col2"]
    ),
    DQDatasetRule(
        criticality="error",
        check_func=check_funcs.is_aggr_not_greater_than,
        column="col1",
        check_func_kwargs={"aggr_type": "count", "limit": 10},
    ),
    DQDatasetRule(
        criticality="error",
        check_func=check_funcs.is_aggr_not_less_than,
        column="col1",
        check_func_kwargs={"aggr_type": "avg", "limit": 1.2},
    ),
]

schema = ("col1: int, col2: int, col3: int, col4 int, col5: map<string, string>,"
          " col6: array<string>, col7: struct<field1: int>")
input_df = spark.createDataFrame([
    [1, 3, 3, None, {"key1": ""}, [""], {"field1": 1}],
    [3, None, 4, 1, {"key1": None}, [None], {"field1": None}],
    [None, None, None, None, None, None, None],
], schema)

# Option 1: apply quality rules and quarantine invalid records
valid_df, quarantine_df = dq_engine.apply_checks_and_split(input_df, checks)
valid_df.show()
quarantine_df.show()

# Option 2: apply quality rules and annotate invalid records as additional columns (`_warning` and `_error`)
valid_and_quarantine_df = dq_engine.apply_checks(input_df, checks)
valid_and_quarantine_df.show()

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

# validate the checks
status = dq_engine.validate_checks(checks)
assert not status.has_errors
