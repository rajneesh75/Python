import sys
from pyspark.sql import SparkSession

print("Driver Python:", sys.executable)


spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()
print(spark)

rdd = spark.sparkContext.parallelize([1,2,3,4])
print(rdd.map(lambda x: x * 2).collect())
