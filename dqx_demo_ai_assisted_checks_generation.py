from databricks.connect import DatabricksSession
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.labs.dqx.config import LLMModelConfig, InputConfig
from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient

model_name = "databricks/databricks-claude-sonnet-4-5"
user_requirement = "customername should not start with s and account balance should be positive"
default_table_name = "samples.tpch.customer"

spark = DatabricksSession.builder.serverless().getOrCreate()
# Initialize the DQX engine
ws = WorkspaceClient()
dq_engine = DQEngine(ws, spark)

# Creating model config with optional model name (default Databricks Foundational
# model endpoint is used if not provided)
llm_model_config = LLMModelConfig(model_name=model_name)
generator = DQGenerator(ws, llm_model_config=llm_model_config)

checks = generator.generate_dq_rules_ai_assisted(user_input=user_requirement)
print("======== Generated checks =========")
print(checks)

checks = generator.generate_dq_rules_ai_assisted(user_input=user_requirement,
                                                 input_config=InputConfig(location=default_table_name))
print("======== Generated checks =========")
print(checks)

# Profile Samples Data
profiler = DQProfiler(ws)
summary_stats, profiles = profiler.profile_table(InputConfig(location=default_table_name))

# No user requirement provided
checks = generator.generate_dq_rules_ai_assisted(summary_stats=summary_stats)