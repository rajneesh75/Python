from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
df = spark.read.csv("customers-100.csv", header=True)
print(df.show(10, truncate=False))