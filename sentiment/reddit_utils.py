import praw
from prawcore.exceptions import NotFound, ResponseException

# Configure your Reddit API credentials (replace with your actual values)
reddit = praw.Reddit(
    client_id='qE7wVTTUQSxLfwQKRObQwg',
    client_secret='85QnOfYqWtKjVbpP7MvD80d_SCjreg',
    user_agent='RedUsr'
)


def fetch_reddit_posts(query, mode="subreddit"):
    try:
        posts = []
        if mode == "subreddit":
            submissions = reddit.subreddit(query).new(limit=5)
        elif mode == "keyword":
            # Use broader search parameters
            submissions = reddit.subreddit("all").search(
                query,
                sort="relevance",
                time_filter="all",
                limit=5
            )
        else:
            raise Exception("Invalid search mode specified.")

        for submission in submissions:
            # ... same logic for extracting media, title, selftext ...
            posts.append({
                'title': submission.title,
                'selftext': submission.selftext,
                'media_url': None,  # or handle media as you do
            })
        return posts
    except NotFound:
        raise Exception("Subreddit not found. Please enter a valid subreddit name.")
    except ResponseException:
        raise Exception("There was an issue with the response from Reddit. Please try again later.")
    except Exception as e:
        raise Exception("An unexpected error occurred while fetching Reddit posts: " + str(e))



# import praw
# from prawcore.exceptions import NotFound, ResponseException
#
# # Configure Reddit API credentials
# reddit = praw.Reddit(
#     client_id="qE7wVTTUQSxLfwQKRObQwg",
#     client_secret="85QnOfYqWtKjVbpP7MvD80d_SCjreg",
#     user_agent="RedUsr"
# )
#
# def fetch_reddit_posts(query, mode="subreddit", limit=5):
#     """Fetches Reddit posts based on a subreddit or keyword search."""
#     try:
#         if mode == "subreddit":
#             submissions = reddit.subreddit(query).new(limit=limit)
#         elif mode == "keyword":
#             submissions = reddit.subreddit("all").search(query, sort="relevance", time_filter="all", limit=limit)
#         else:
#             raise ValueError("Invalid search mode. Choose 'subreddit' or 'keyword'.")
#
#         posts = []
#         for submission in submissions:
#             media_url = None
#             if submission.url and ("i.redd.it" in submission.url or "imgur.com" in submission.url):
#                 media_url = submission.url  # Extract image/video links
#
#             posts.append({
#                 "title": submission.title,
#                 "selftext": submission.selftext[:500],  # Limit text size for better display
#                 "media_url": media_url,
#                 "score": submission.score,
#                 "num_comments": submission.num_comments,
#                 "permalink": f"https://www.reddit.com{submission.permalink}"
#             })
#
#         return posts
#
#     except NotFound:
#         raise Exception("Subreddit not found. Please enter a valid subreddit name.")
#     except ResponseException:
#         raise Exception("There was an issue with Reddit's response. Please try again later.")
#     except Exception as e:
#         raise Exception(f"Error fetching Reddit posts: {e}")


