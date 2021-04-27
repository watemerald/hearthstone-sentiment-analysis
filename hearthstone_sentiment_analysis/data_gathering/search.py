import requests
import jsonlines
from .utils import settings

from typing import List, Optional, Any


def get_tweets_by_users(
    user_list: List[str],
    session: Optional[requests.Session] = None,
    max_results: int = 100,
):
    if session is None:
        session = requests.Session()
        session.headers["Authorization"] = f"Bearer {settings.TWITTER_BEARER_TOKEN}"
    with jsonlines.open("data/tweets.jsonl", mode="a") as writer:
        writer: Any
        for user in user_list:
            response = session.get(
                "https://api.twitter.com/2/tweets/search/recent",
                params={
                    "query": f"from:{user} -is:retweet",
                    "max_results": max_results,
                    "expansions": "author_id",
                    "tweet.fields": "public_metrics,created_at",
                },
            )
            writer.write(response.json())


def get_tweets_by_hashtags(
    hashtags: List[str],
    session: Optional[requests.Session] = None,
    max_results: int = 100,
):
    if session is None:
        session = requests.Session()
        session.headers["Authorization"] = f"Bearer {settings.TWITTER_BEARER_TOKEN}"
    with jsonlines.open("data/tweets.jsonl", mode="a") as writer:
        writer: Any
        for hashtag in hashtags:
            response = session.get(
                "https://api.twitter.com/2/tweets/search/recent",
                params={
                    "query": f"#{hashtag} -is:retweet",
                    "max_results": max_results,
                    "expansions": "author_id",
                    "tweet.fields": "public_metrics,created_at",
                },
            )
            writer.write(response.json())