from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.sdk import WorkspaceClient

from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless().getOrCreate()

# Initialize the generator
ws = WorkspaceClient()
generator = DQGenerator(workspace_client=ws)

# Generate rules from natural language description
user_input = """
Username should not start with 's' if age is less than 18.
All users must have a valid email address.
Age should be between 0 and 120.
"""

checks = generator.generate_dq_rules(user_input)

print(checks)
