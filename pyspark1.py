from pyspark.sql import SparkSession
spark1 = SparkSession.builder.master("local[*]").appName("test1").getOrCreate()
print(spark1.sparkContext)
spark1.sparkContext.stop()


