import yaml
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx.engine import DQEngine
from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.config import LLMModelConfig, InputConfig
from databricks.labs.dqx.rule import DQDatasetRule
from databricks.labs.dqx import check_funcs
import pyspark.sql.functions as F
import logging

logging.basicConfig(level=logging.DEBUG)

spark = DatabricksSession.builder.serverless().getOrCreate()
ws = WorkspaceClient()
dq_engine = DQEngine(ws)

# define LLM model config
llm_model_config = LLMModelConfig(model_name="databricks-claude-sonnet-4")

# Use existing sample table
input_table_name = "workspace.bronze.products"

input_df = spark.table(input_table_name)

# Preview the table structure
input_df.show()

profiler = DQProfiler(ws, spark, llm_model_config=llm_model_config)
pk_result = profiler.detect_primary_keys_with_llm(input_config=InputConfig(location=input_table_name))
pk_columns = pk_result.get('primary_key_columns')

checks = [
    DQDatasetRule(
        criticality="error",
        check_func=check_funcs.compare_datasets,
        columns=pk_columns,
        check_func_kwargs={
            "ref_columns": pk_columns,
            "ref_df_name": "ref_df_key",
        },
    ),
]

# prepare reference DataFrame
ref_df = input_df.withColumn("c_name", F.when(F.col("c_custkey") == F.lit("412445"), "fake").otherwise(F.col("c_name")))
ref_dfs = {"ref_df_key": ref_df}

valid_df, quarantine_df = dq_engine.apply_checks_and_split(input_df, checks, ref_dfs=ref_dfs)
quarantine_df.show()

profiler = DQProfiler(ws, spark)
generator = DQGenerator(ws, spark)



# run one of the profiling methods
summary_stats, profiles = profiler.profile(input_df)

print("=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)
print(summary_stats)

print("=" * 80)
print("PROFILES")
print("=" * 80)
print(profiles)

checks = generator.generate_dq_rules(profiles)  # with default level "error"
print(yaml.safe_dump(checks))
