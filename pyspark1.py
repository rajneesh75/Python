from pyspark.sql import SparkSession
spark1 = SparkSession.builder.master("local[*]").appName("test1").getOrCreate()
print(spark1.sparkContext)
spark1.sparkContext.stop()
spark2 = SparkSession.builder.master("local[*]").appName("test2").getOrCreate()
print(spark2.sparkContext)

