import os
from dotenv import load_dotenv

from databricks.connect import DatabricksSession
from databricks.labs.dqx.config import InputConfig, LLMModelConfig
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.sdk import WorkspaceClient
import logging

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

spark = (
    DatabricksSession.builder
    .serverless(True)
    .getOrCreate()
)

print("Spark Version:", spark.version)
ws = WorkspaceClient()

# --------------------------------------------------
# DQX LLM configuration
# --------------------------------------------------

llm_config = LLMModelConfig(
    model_name="gpt-5.6",
    api_key=os.getenv("DATABRICKS_TOKEN"),
    api_base=(
        "https://dbc-c379cba2-8489.cloud.databricks.com"
        "/ai-gateway/openai/v1"
    ),
    temperature=0.0,
    max_tokens=1000,
    timeout=60,
    max_retries=3,
)

generator = DQGenerator(workspace_client=ws, spark=spark, llm_model_config=llm_config, )

profiler = DQProfiler(ws)
summary_stats, profiles = profiler.profile_table(input_config=InputConfig(location="workspace.bronze.customers"))
print("Summary statistics:")
print(summary_stats)

# --------------------------------------------------
# AI-assisted rule generation
# --------------------------------------------------

checks = generator.generate_dq_rules_ai_assisted(
    user_input="Validate customers data for anomalies and business rules",
    summary_stats=summary_stats,
)

print("\nGenerated checks:")
print(checks)

print(f"\nGenerated {len(checks)} quality checks")
