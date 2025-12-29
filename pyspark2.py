from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyFirstSparkJob") \
    .getOrCreate()
spark.sparkContext.setLogLevel("INFO")
print(spark.sparkContext)