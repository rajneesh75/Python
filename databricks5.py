from databricks.connect import DatabricksSession
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

spark = DatabricksSession.builder.serverless().getOrCreate()
print(spark.version)
df = spark.read.table("workspace.bronze.products")
df.show()
