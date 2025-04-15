#from Spark_App import pipeline_class
import pyspark
from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.appName("Dug").getOrCreate()
    df = spark.read.text("high_popularity_spotify_data.csv")
    print(df.show())

if __name__ == "__main__":
    main()
