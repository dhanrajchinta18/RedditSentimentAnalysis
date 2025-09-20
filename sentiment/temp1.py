from spark_session import get_spark_session
from pyspark.sql.types import StructType, StructField, StringType
file_path = "C:/reddit_sentiment_app/data.csv"

spark = get_spark_session()

schema = StructType([
    StructField("Id", StringType(), True),
    StructField("Title", StringType(), True),
    StructField("Author", StringType(), True),
    StructField("Subreddit", StringType(), True),
    StructField("Score", StringType(), True),  # Adjust type if needed
    StructField("Permalink", StringType(), True),
    StructField("Creation Time", StringType(), True),
    StructField("Number of Comments", StringType(), True),
    StructField("Upvote Ratio", StringType(), True),
    StructField("URL", StringType(), True),
    StructField("Post ID", StringType(), True),
    StructField("Is Original Content", StringType(), True),
    StructField("Flair", StringType(), True)
                    # Skipping the Comments column since it’s problematic
    ])
df = spark.read \
    .format("csv") \
    .option("header", True) \
    .option("multiLine", True) \
    .option("quote", "\"") \
    .option("escape", "\"") \
    .option("sep", ",") \
    .schema(schema) \
    .load(file_path)


                # Sample aggregation: count posts per Subreddit
result_df = df.groupBy("Subreddit").count()

result_df.show(20, truncate=False)
df.printSchema()
