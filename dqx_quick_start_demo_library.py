from pyspark.sql import Row
from databricks.connect import DatabricksSession
import yaml
from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx.rule import DQRowRule, DQDatasetRule, DQForEachColRule, Criticality
from databricks.labs.dqx import check_funcs

spark = DatabricksSession.builder.serverless().getOrCreate()


# Create a sample DataFrame
new_users = [
    Row(id=1, age=23, country='Germany'),
    Row(id=2, age=30, country='France'),
    Row(id=3, age=16, country='Germany'),  # Invalid -> age - less than 18
    Row(id=None, age=29, country='France'),  # Invalid -> id - NULL
    Row(id=4, age=29, country=''),  # Invalid -> country - Empty
    Row(id=5, age=23, country='Italy'),  # Invalid -> country - not in allowed
    Row(id=6, age=123, country='France'),  # Invalid -> age - greater than 120
    Row(id=2, age=23, country='Germany'),  # duplicated id
]

new_users_df = spark.createDataFrame(new_users)

checks_from_yaml = yaml.safe_load("""
# 1. Ensure id, age, country are not null or empty (error-level)
- check:
    function: is_not_null_and_not_empty
    for_each_column:  # define check for multiple columns at once
      - id
      - age
      - country
  criticality: error

# 2. Warn if age is outside [18, 120] for Germany or France
- check:
    function: is_in_range
    filter: country in ['Germany', 'France']
    arguments:
      column: age  # define check for a single column
      min_limit: 18
      max_limit: 120
  criticality: warn
  name: age_not_in_range  # optional check name, auto-generated if not provided

# 3. Warn if country is not Germany or France
- check:
    function: is_in_list
    for_each_column:
      - country
    arguments:
      allowed:
        - Germany
        - France
  criticality: warn

# 4. Error if id is not unique across the dataset
- check:
    function: is_unique
    arguments:
      columns:
        - id
  criticality: error
""")

status = DQEngine.validate_checks(checks_from_yaml)
print(f"Checks from YAML: {status}")
ws = WorkspaceClient()
dq_engine = DQEngine(ws)

validated_df = dq_engine.apply_checks_by_metadata(new_users_df, checks_from_yaml)
print("Validated DataFrame:")
validated_df.show()

valid_df, invalid_df = dq_engine.apply_checks_by_metadata_and_split(new_users_df, checks_from_yaml)
print("Valid DataFrame:")
valid_df.show()
print("Invalid DataFrame:")
invalid_df.show()

checks = [
    # 1. Ensure id, age, country are not null or empty (error-level)
    *DQForEachColRule(
        columns=["id", "age", "country"],
        check_func=check_funcs.is_not_null_and_not_empty,
        criticality=Criticality.ERROR.value,
    ).get_rules(),

    # 2. Warn if age is outside [18, 120] for Germany or France
    DQRowRule(
        column="age",
        check_func=check_funcs.is_in_range,
        check_func_kwargs={"min_limit": 18, "max_limit": 120},
        filter="country IN ('Germany', 'France')",
        criticality=Criticality.WARN.value,
        name="age_not_in_range",
    ),

    # 3. Warn if country is not Germany or France
    *DQForEachColRule(
        columns=["country"],
        check_func=check_funcs.is_in_list,
        criticality=Criticality.WARN.value,
        check_func_kwargs={"allowed": ["Germany", "France"]},
    ).get_rules(),

    # 4. Error if id is not unique across the dataset
    DQDatasetRule(
        columns=["id"],
        check_func=check_funcs.is_unique,
        criticality=Criticality.ERROR.value,
    ),
]

validated_df = dq_engine.apply_checks(new_users_df, checks)
print("Validated DataFrame:")
validated_df.show()
valid_df, invalid_df = dq_engine.apply_checks_and_split(new_users_df, checks)
print("Valid DataFrame:")
valid_df.show()
print("Invalid DataFrame:")
invalid_df.show()
