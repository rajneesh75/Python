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
    "CREATE OR REPLACE FUNCTION get_customer_billing_and_subscriptions"
    " (customer_id_input BIGINT COMMENT 'customer ID used to retrieve orders, billing and subscription')"
    " RETURNS TABLE(customer_id BIGINT, subscription_id BIGINT, service_type STRING, plan_name STRING,"
    " plan_tier STRING, monthly_charge BIGINT, start_date DATE, contract_length_months BIGINT, status STRING,"
    " autopay_enabled BOOLEAN, total_billed DOUBLE, total_paid DOUBLE, total_late_payments BIGINT,"
    " total_late_fees DOUBLE, latest_payment_status STRING ) COMMENT"
    " 'Returns subscription and billing details for a customer.'"
    " RETURN( SELECT s.customer_id, s.subscription_id, s.service_type, s.plan_name, s.plan_tier,"
    " s.monthly_charge, s.start_date, s.contract_length_months, s.status, s.autopay_enabled,"
    " COALESCE(b.total_billed, 0), COALESCE(b.total_paid, 0), COALESCE(b.total_late_payments, 0),"
    " COALESCE(b.total_late_fees, 0), COALESCE(b.latest_payment_status, 'N/A')"
    " FROM subscriptions s LEFT JOIN(SELECT subscription_id, customer_id, SUM(total_amount)"
    " AS total_billed, SUM(payment_amount) AS total_paid,"
    " COUNT_IF(payment_date > due_date OR payment_status = 'Late') AS total_late_payments,"
    " SUM(CASE WHEN payment_date > due_date OR payment_status = 'Late' THEN total_amount - payment_amount"
    " ELSE 0 END) AS total_late_fees, MAX(payment_status) AS latest_payment_status FROM billing WHERE"
    " customer_id = customer_id_input GROUP BY subscription_id, customer_id) b ON"
    " s.subscription_id = b.subscription_id WHERE s.customer_id = customer_id_input);")

df.show()

df = spark.sql(
    "SELECT * FROM get_customer_billing_and_subscriptions("
    " (SELECT customer_id FROM get_customer_by_email('john21@example.net'))"
    ");"
)

df.show()
