# sentiment/spark_utils.py

from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .spark_session import get_spark_session

analyzer = SentimentIntensityAnalyzer()


def compute_sentiment(text):
    if text:
        score = analyzer.polarity_scores(text)['compound']
        if score >= 0.05:
            return "positive"
        elif score <= -0.05:
            return "negative"
        else:
            return "neutral"
    return "neutral"


sentiment_udf = udf(compute_sentiment, StringType())


def process_posts(posts):
    spark = get_spark_session()

    # Define a schema matching your dictionaries
    schema = StructType([
        StructField("title", StringType(), True),
        StructField("selftext", StringType(), True),
        StructField("media_url", StringType(), True)
    ])

    # Create a DataFrame with the explicit schema
    df = spark.createDataFrame(posts, schema=schema)

    # Apply sentiment analysis on the post title
    df = df.withColumn("sentiment", sentiment_udf(df.title))

    # Convert back to list of dictionaries
    analyzed_posts = df.toPandas().to_dict(orient='records')
    return analyzed_posts




# from pyspark.sql.types import StructType, StructField, StringType
# from pyspark.sql.functions import udf
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from .spark_session import get_spark_session
# import logging
#
# logger = logging.getLogger(__name__)
#
# def process_posts(posts):
#     if not posts: return []
#
#     try:
#         df = get_spark_session().createDataFrame(posts, schema=StructType([
#             StructField("title", StringType(), True),
#             StructField("selftext", StringType(), True),
#             StructField("media_url", StringType(), True)
#         ]))
#
#         analyzer = SentimentIntensityAnalyzer()
#         sentiment_udf = udf(lambda text: "positive" if (s := analyzer.polarity_scores(text)['compound']) >= 0.05
#                             else "negative" if s <= -0.05 else "neutral", StringType())
#
#         return df.withColumn("title_sentiment", sentiment_udf(df.title))\
#                  .withColumn("selftext_sentiment", sentiment_udf(df.selftext))\
#                  .toPandas().to_dict(orient="records")
#
#     except Exception as e:
#         logger.error(f"Error processing posts: {e}")
#         return []


# def process_posts(posts):
#     # Convert list of dicts into an RDD of Rows
#     rdd = spark.sparkContext.parallelize([Row(**post) for post in posts])
#     df = spark.createDataFrame(rdd)
#
#     # Apply sentiment analysis on the post title (or selftext if preferred)
#     df = df.withColumn("sentiment", sentiment_udf(df.title))
#
#     # Collect results back to a list of dictionaries
#     analyzed_posts = df.toPandas().to_dict(orient='records')
#     return analyzed_posts
