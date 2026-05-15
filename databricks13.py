from databricks.labs.dqx import check_funcs
from databricks.labs.dqx.rule import DQRowRule, DQDatasetRule, DQForEachColRule
from pyspark.sql import functions as F
from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless().getOrCreate()
df = spark.read.table("workspace.bronze.customers_cdc1")


checks = [
    DQRowRule(  # check for a single column
        name="col3_is_null_or_empty",
        criticality="warn",
        check_func=check_funcs.is_not_null_and_not_empty,
        column="col3",
    ),

    *DQForEachColRule(  # apply the same checks to multiple columns
        columns=["col1", "col2"],
        criticality="error",
        check_func=check_funcs.is_not_null).get_rules(),

    DQRowRule(  # check with a filter
        name="col_4_is_null_or_empty",
        criticality="warn",
        filter="col1 < 3",
        check_func=check_funcs.is_not_null_and_not_empty,
        column="col4",
    ),

    DQRowRule(  # check with user metadata
        name="col_5_is_null_or_empty",
        criticality="warn",
        check_func=check_funcs.is_not_null_and_not_empty,
        column="col5",
        user_metadata={
            "check_type": "completeness",
            "responsible_data_steward": "someone@email.com"
        },
    ),

    DQRowRule(  # provide check func arguments using positional arguments
        criticality="warn",
        check_func=check_funcs.is_in_list,
        column="col1",
        check_func_args=[[1, 2]],
    ),

    DQRowRule(  # provide check func arguments using keyword arguments
        criticality="warn",
        check_func=check_funcs.is_in_list,
        column="col2",
        check_func_kwargs={"allowed": [1, 2]},
    ),

    DQRowRule(  # check for a struct field
        # use "error" criticality if not provided
        check_func=check_funcs.is_not_null,
        column="col7.field1",
    ),

    DQRowRule(  # check for a map element
        criticality="error",
        check_func=check_funcs.is_not_null,
        column=F.try_element_at("col5", F.lit("key1")),
    ),

    DQRowRule(  # check for an array element
        criticality="error",
        check_func=check_funcs.is_not_null,
        column=F.try_element_at("col6", F.lit(1)),
    ),

    DQDatasetRule(  # check uniqueness of composite key
        criticality="error",
        check_func=check_funcs.is_unique,
        columns=["col1", "col2"]
    ),

    DQDatasetRule(  # dataset check working across group of rows
        criticality="error",
        check_func=check_funcs.is_aggr_not_greater_than,
        column="col1",
        check_func_kwargs={"aggr_type": "count", "group_by": ["col2"], "limit": 10},
    ),

    DQDatasetRule(  # dataset check working across group of rows
        criticality="error",
        check_func=check_funcs.is_aggr_not_less_than,
        column="col1",
        check_func_kwargs={"aggr_type": "avg", "group_by": ["col2"], "limit": 1.2},
    ),

    DQDatasetRule(  # dataset check working across group of rows
        criticality="error",
        check_func=check_funcs.is_aggr_equal,
        column="col1",
        check_func_kwargs={"aggr_type": "count", "group_by": ["col2"], "limit": 5},
    ),

    DQDatasetRule(  # dataset check working across group of rows
        criticality="error",
        check_func=check_funcs.is_aggr_not_equal,
        column="col1",
        check_func_kwargs={"aggr_type": "avg", "group_by": ["col2"], "limit": 10.5},
    ),

    DQDatasetRule(  # dataset check for distinct value count for groups (each group should have 1 value)
        criticality="error",
        check_func=check_funcs.is_aggr_not_greater_than,
        column="country_code",
        check_func_kwargs={
            "aggr_type": "count_distinct",  # Exact distinct count
            "group_by": ["country"],
            "limit": 1
        },
    ),

    DQDatasetRule(  # dataset check for standard deviation for groups
        criticality="warn",
        check_func=check_funcs.is_aggr_not_greater_than,
        column="temperature",
        check_func_kwargs={
            "aggr_type": "stddev",
            "group_by": ["machine_id"],
            "limit": 5.0
        },
    ),

    DQDatasetRule(  # dataset check for percentile with the percentile value passed using aggr_params
        criticality="error",
        check_func=check_funcs.is_aggr_not_greater_than,
        column="latency_ms",
        check_func_kwargs={
            "aggr_type": "percentile",
            "aggr_params": {"percentile": 0.95},
            "limit": 1000
        },
    ),
]