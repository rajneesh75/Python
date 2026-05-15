from databricks.connect import DatabricksSession
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.sdk import WorkspaceClient

# Initialize the generator
ws = WorkspaceClient()
spark = DatabricksSession.builder.serverless().getOrCreate()
generator = DQGenerator(workspace_client=ws, spark=spark)

# Generate rules from natural language description
user_input = """
Username should not start with 's' if age is less than 18.
All users must have a valid email address.
Age should be between 0 and 120.
"""

checks = generator.generate_dq_rules_ai_assisted(user_input=user_input)

print(checks)