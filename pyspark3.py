from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("MyFirstSparkJob").getOrCreate()
spark.sparkContext.setLogLevel("INFO")
data = [("Raj", 25), ("Neha", 29), ("Vikram", 31)]
df = spark.createDataFrame(data, ["name", "age"])
df.show(1, truncate=False)

