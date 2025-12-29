from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel("INFO")
df = spark.read.csv("customers-100.csv", header=True)
print(df.show(10, truncate=False))
