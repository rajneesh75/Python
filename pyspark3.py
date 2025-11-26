from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("MyFirstSparkJob").getOrCreate()

data = [("Raj", 25), ("Neha", 29), ("Vikram", 31)]
df = spark.createDataFrame(data, ["name", "age"])
df.show()

