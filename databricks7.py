import yaml
from databricks.sdk import WorkspaceClient
import base64
from databricks.sdk.service.workspace import ExportFormat
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.connect import DatabricksSession


spark = DatabricksSession.builder.serverless().getOrCreate()

ws = WorkspaceClient()

workspace_path = "/Repos/rajneesh75@gmail.com/databricks/customer_data_contract.yml"
local_path = "customer_data_contract.yml"

# Export Workspace file (as SOURCE)
exported = ws.workspace.export(workspace_path, format=ExportFormat.SOURCE)

# Decode and write to local file
with open(local_path, "wb") as f:
    f.write(base64.b64decode(exported.content))

print("Saved locally:", local_path)

# Load YAML contract
with open(local_path, "r") as f:
    contract = yaml.safe_load(f)

generator = DQGenerator(ws)
rules = generator.generate_dq_rules(contract)
print("Generated rules:", len(rules))
print(rules)
