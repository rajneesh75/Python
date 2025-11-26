from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MyFirstSparkJob").getOrCreate()

rdd = spark.sparkContext.parallelize([1, 2])
print(rdd.values())
rdd2 = rdd.map(lambda x: x * 10)
print(rdd2.collect())
