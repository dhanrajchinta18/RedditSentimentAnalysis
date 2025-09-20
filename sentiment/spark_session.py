# sentiment/spark_session.py

from pyspark.sql import SparkSession

def get_spark_session():
    return SparkSession.builder \
        .appName("RedditSentimentAnalysis") \
        .master("local[*]") \
        .getOrCreate()
