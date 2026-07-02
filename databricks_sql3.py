from databricks.connect import DatabricksSession
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

spark = (
    DatabricksSession.builder
    .host("https://dbc-c379cba2-8489.cloud.databricks.com")
    .token(str(os.getenv("DATABRICKS_TOKEN")))
    .serverless(True)
    .getOrCreate()
)
print("Spark Version:", spark.version)
spark.sql("USE main.dbdemos_ai_agent")

df = spark.sql(
    "CREATE OR REPLACE FUNCTION get_customer_by_email"
    "(email_input STRING COMMENT 'customer email used to retrieve customer information')"
    "RETURNS TABLE (customer_id BIGINT, first_name STRING, last_name STRING, email STRING, phone STRING,"
    "address STRING, city STRING, state STRING, zip_code STRING, customer_segment STRING,"
    "registration_date DATE, customer_status STRING, loyalty_tier STRING, tenure_years DOUBLE,"
    "churn_risk_score BIGINT, customer_value_score BIGINT )"
    "COMMENT 'Returns the customer record matching the provided email address. "
    "Includes its ID, firstname, lastname and more.'"
    "RETURN (SELECT * FROM customers WHERE email = email_input LIMIT 1);")

df.show()
