
# sentiment/views.py
import logging
import time
import pandas as pd
from django.shortcuts import render
from .reddit_utils import fetch_reddit_posts
from .spark_utils import process_posts
from .spark_session import get_spark_session
from pyspark.sql.types import StructType, StructField, StringType

logger = logging.getLogger(__name__)

def index(request):
    context = {}
    if request.method == 'POST':
        search_mode = request.POST.get('search_mode', 'subreddit')
        start_time = time.time()
        query = request.POST.get('query')
        try:
            posts = fetch_reddit_posts(query, mode=search_mode)
            # Ensure SparkSession is created on the driver
            spark = get_spark_session()
            analyzed_posts = process_posts(posts)
            context['query'] = query
            context['posts'] = analyzed_posts
        except Exception as e:
            logger.error("Error processing request for query '%s' (mode: %s): %s", query, search_mode, str(e))
            context['error'] = str(e)
        end_time = time.time()
        context['elapsed_time'] = round(end_time - start_time, 2)
    return render(request, 'sentiment/index.html', context)


def demo(request):
    """
    Demonstrates processing a dataset with and without Spark.
    Assumes the CSV file is located at data/reddit_demo.csv.
    Performs a simple aggregation: counting posts per Subreddit.
    """
    context = {}
    if request.method == 'POST':
        method = None
        # Determine which button was pressed by checking the name attribute
        if "spark" in request.POST:
            method = "spark"
        elif "no_spark" in request.POST:
            method = "no_spark"

        if method:
            start_time = time.time()
            file_path = "C:/reddit_sentiment_app/top_reddit_posts.csv"  # Ensure your CSV is in this location

            if method == "spark":
                # Process using Spark
                spark = get_spark_session()
                # Read CSV with header and schema inference
                schema = StructType([
                    StructField("Id",StringType(), True),
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
                    .option("encoding", "macroman") \
                    .option("mode", "DROPMALFORMED") \
                    .schema(schema) \
                    .load(file_path)
                # Sample aggregation: count posts per Subreddit
                result_df = df.groupBy("Subreddit").count()
                # Collect results to driver as a list of dictionaries
                result = result_df.collect()
                processed_data = [row.asDict() for row in result]
            else:
                # Process without Spark using Pandas
                df = pd.read_csv(file_path)
                # Sample aggregation: count posts per Subreddit
                result = df.groupby("Subreddit").size().reset_index(name="count")
                processed_data = result.to_dict(orient="records")

            end_time = time.time()
            context['processed_data'] = processed_data
            context['elapsed_time'] = round(end_time - start_time, 2)
            context['method'] = method
    return render(request, 'sentiment/demo.html', context)


# import logging
# import time
# from django.shortcuts import render
# from .reddit_utils import fetch_reddit_posts
# from .spark_utils import process_posts
# from .spark_session import get_spark_session
#
# logger = logging.getLogger(__name__)
#
#
# def index(request):
#     context = {}
#
#     if request.method == 'POST':
#         query = request.POST.get('query')
#         search_mode = request.POST.get('search_mode', 'subreddit')
#         start_time = time.time()
#
#         try:
#             posts = fetch_reddit_posts(query, mode=search_mode)
#             spark = get_spark_session()  # Ensure SparkSession is created
#             context['posts'] = process_posts(posts)
#             context['query'] = query
#         except Exception as e:
#             logger.error(f"Error processing request for '{query}' (mode: {search_mode}): {e}")
#             context['error'] = str(e)
#
#         context['elapsed_time'] = round(time.time() - start_time, 2)
#
#     return render(request, 'sentiment/index.html', context)

# from django.shortcuts import render
# from .reddit_utils import fetch_reddit_posts
# from .spark_utils import process_posts
# from .spark_session import get_spark_session
# import logging
# import time
# logger = logging.getLogger(__name__)
#
# def index(request):
#     context = {}
#     if request.method == 'POST':
#         search_mode = request.POST.get('search_mode', 'subreddit')
#         query = request.POST.get('query')
#         start_time = time.time()
#         try:
#             posts = fetch_reddit_posts(query, mode=search_mode)
#             # Ensure SparkSession is created on the driver
#             spark = get_spark_session()
#             analyzed_posts = process_posts(posts)
#             context['search_query'] = query
#             context['posts'] = analyzed_posts
#         except Exception as e:
#             logger.error("Error processing request for query '%s' (mode: %s): %s", query, search_mode, str(e))
#             context['error'] = str(e)
#         end_time = time.time()
#         context['elapsed_time'] = round(end_time - start_time, 2)
#     return render(request, 'sentiment/index.html', context)



