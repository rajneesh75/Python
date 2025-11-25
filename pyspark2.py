from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyFirstSparkJob") \
    .getOrCreate()

print(spark)