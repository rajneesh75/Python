import tempfile
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
id: urn:datacontract:ecommerce:orders
name: E-Commerce Orders
version: 1.0.0
status: active
domain: ecommerce
dataProduct: orders_data_product
tenant: Data Engineering Team

description:
  purpose: Customer order data for e-commerce platform
  usage: Demonstrate DQX rule generation from ODCS v3.x contracts

tags:
  - ecommerce
  - orders
  - demo

schema:
  - name: orders
    physicalName: orders_table
    physicalType: table
    description: Customer orders table
    
    properties:
      - name: order_id
        logicalType: string
        physicalType: varchar(12)
        description: Unique order identifier
        required: true
        unique: true
        primaryKey: true
        logicalTypeOptions:
          pattern: '^ORD-[0-9]{8}$'
      
      - name: customer_email
        logicalType: string
        physicalType: varchar(100)
        description: Customer email address
        required: true
        logicalTypeOptions:
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
      
      - name: order_date
        logicalType: date
        physicalType: date
        description: Order placement date
        required: true
        logicalTypeOptions:
          format: 'yyyy-MM-dd'
      
      - name: order_total
        logicalType: number
        physicalType: decimal(10,2)
        description: Total order amount
        required: true
        logicalTypeOptions:
          minimum: 0.01
          maximum: 100000.00
        quality:
          # Field-level quality check (explicit DQX rule)
          - type: custom
            engine: dqx
            description: Warn on unusually high order totals
            implementation:
              criticality: warn
              name: order_total_reasonable_check
              check:
                function: is_not_greater_than
                arguments:
                  column: order_total
                  limit: 50000
      
      - name: order_status
        logicalType: string
        physicalType: varchar(20)
        description: Current order status
        required: true
        logicalTypeOptions:
          pattern: '^(pending|confirmed|shipped|delivered|cancelled)$'
      
      - name: quantity
        logicalType: integer
        physicalType: int
        description: Number of items
        required: true
        logicalTypeOptions:
          minimum: 1
          maximum: 1000
      
      - name: discount_percentage
        logicalType: number
        physicalType: decimal(5,2)
        description: Discount applied
        required: false
        logicalTypeOptions:
          minimum: 0.0
          maximum: 100.0
    
    # Dataset-level quality checks (explicit DQX rules and text-based expectations)
    quality:
      # Example 1: Custom DQX rule - Check dataset is not empty
      - type: custom
        engine: dqx
        description: Ensure orders dataset contains data
        implementation:
          criticality: error
          name: orders_dataset_not_empty
          check:
            function: is_aggr_not_less_than
            arguments:
              column: order_id
              limit: 1
              aggr_type: count
      
      # Example 2: Text-based expectation (AI-assisted rule generation)
      - type: text
        description: "For rows where order_total > 10000, the order_status column 
        must be either 'confirmed' or 'shipped'"
      
      # Example 3: Another text-based expectation for cross-field validation
      - type: text
        description: "For rows where discount_percentage > 50, the discount_percentage must be less than or equal to 75"
"""

# Parse contract and write to temporary file
# Parse YAML
contract_dict = yaml.safe_load(contract_yaml)

# Define schema
schema = T.StructType([
    T.StructField("order_id", T.StringType(), True),
    T.StructField("customer_email", T.StringType(), True),
    T.StructField("order_date", T.DateType(), True),
    T.StructField("order_total", T.DecimalType(10, 2), True),
    T.StructField("order_status", T.StringType(), True),
    T.StructField("quantity", T.IntegerType(), True),
    T.StructField("discount_percentage", T.DecimalType(5, 2), True)
])

# Sample data with mix of valid and invalid records
data = [
    # Valid record
    ("ORD-12345678", "customer@example.com", date(2024, 1, 15), Decimal("99.99"), "confirmed", 2, Decimal("10.0")),
    # Valid record
    ("ORD-87654321", "another@test.com", date(2024, 1, 16), Decimal("150.50"), "shipped", 1, Decimal("5.0")),
    # Invalid: null required field
    (None, "test@example.com", date(2024, 1, 17), Decimal("75.00"), "pending", 1, Decimal("0.0")),
    # Invalid: pattern mismatch
    ("INVALID", "bad@example.com", date(2024, 1, 18), Decimal("200.00"), "delivered", 3, Decimal("15.0")),
    # Invalid: out of range
    ("ORD-99999999", "valid@test.com", date(2024, 1, 19), Decimal("150000.00"), "confirmed", 2, Decimal("10.0")),
    # Invalid: status not in enum
    ("ORD-11111111", "test@mail.com", date(2024, 1, 20), Decimal("50.00"), "unknown", 1, Decimal("5.0")),
]

df = spark.createDataFrame(data, schema)
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
explicit_count = len([r for r in rules if r.get("user_metadata", {}).get("rule_type") == "explicit"])
text_llm_count = len([r for r in rules if r.get("user_metadata", {}).get("rule_type") == "text_llm"])

print(f"  - {predefined_count} predefined rules (from property constraints)")
print(f"  - {explicit_count} explicit DQX rules")
print(f"  - {text_llm_count} AI-generated rules (from text expectations)")

# Display generated rules
print("========== Generated Rules ==========")

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

print(json.dumps(rules, indent=2, cls=DecimalEncoder))

validation_status = DQEngine.validate_checks(rules)

if validation_status.has_errors:
    print("⚠️  Validation errors found:")
    for error in validation_status.errors:
        print(f"  - {error}")
else:
    print(f"✅ All {len(rules)} rules validated successfully!")

engine = DQEngine(ws)
result_df = engine.apply_checks_by_metadata(df, rules)

# Show results (added columns prefixed with dq_)
result_df.show()
good_df, bad_df = engine.apply_checks_by_metadata_and_split(df, rules)

print(f"Good records: {good_df.count()}")
print(f"Bad records: {bad_df.count()}")

print("\n=== Good Records ===")
good_df.show()

print("\n=== Bad Records ===")
bad_df.show()
