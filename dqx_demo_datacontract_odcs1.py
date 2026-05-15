import yaml
import json
from databricks.sdk import WorkspaceClient
from databricks.connect import DatabricksSession
from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.engine import DQEngine
from datetime import date
from decimal import Decimal
from pyspark.sql import types as T

spark = DatabricksSession.builder.serverless().getOrCreate()
# Initialize the DQX engine
ws = WorkspaceClient()
dq_engine = DQEngine(ws, spark)

# Example data contract (ODCS v3.x format)
contract_yaml = """
kind: DataContract
apiVersion: v3.0.2
id: urn:datacontract:customers
name: customers
version: 1.0.0
status: active
domain: insurance
dataProduct: customers
tenant: Data Engineering Team

tags:
  - customers
  - gold
  - master-data
  - external-reporting
 
# SERVERS
 
servers:
  production:
    type: databricks
    catalog: workspace
    schema: bronze
    table: customers
    format: delta 

schema:
  - name: bronze
    physicalName: customers
    physicalType: table
    description: customers table
    
    properties:    
      - name: customer_id
        type: string
        required: true
        unique: true
        primaryKey: true
        description: Primary identifier for the customer. Trimmed and non-empty.       
        logicalTypeOptions:
          pattern: '^C[0-9]{5}$'
      
      - name: email
        logicalType: string
        physicalType: varchar(50)
        description: Customer email address
        required: true
        logicalTypeOptions:
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'   
"""

# Define schema
schema = T.StructType([
    T.StructField("customer_id", T.StringType(), False),
    T.StructField("customer_email", T.StringType(), True)
])

# Parse contract and write to temporary file

contract_dict = yaml.safe_load(contract_yaml)
df = spark.table("workspace.bronze.customers")
df.show()
# Profile input data
profiler = DQProfiler(ws)
summary_stats, profiles = profiler.profile(df)

# Generate DQX rules from profiles
generator = DQGenerator(workspace_client=ws)
rules = generator.generate_dq_rules(profiles)

print(f"Generated {len(rules)} quality rules from contract")

# Show rule breakdown by type
predefined_count = len([r for r in rules if r.get("user_metadata", {}).get("rule_type") == "predefined"])
# explicit_count = len([r for r in rules if r.get("user_metadata", {}).get("rule_type") == "explicit"])
# text_llm_count = len([r for r in rules if r.get("user_metadata", {}).get("rule_type") == "text_llm"])

print(f"  - {predefined_count} predefined rules (from property constraints)")
# print(f"  - {explicit_count} explicit DQX rules")
# print(f"  - {text_llm_count} AI-generated rules (from text expectations)")

# Display generated rules
print("========== Generated Rules ==========")


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


print(json.dumps(rules, indent=2, cls=DecimalEncoder))
