import json
import os
from datetime import datetime
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel


class PublicMetricsModel(BaseModel):
    retweet_count: int
    reply_count: int
    like_count: int
    quote_count: int


class TweetModel(BaseModel):
    public_metrics: PublicMetricsModel
    text: str
    created_at: datetime
    author_id: int
    id: int


class UserModel(BaseModel):
    id: int
    name: str
    username: str


class IncludesResult(BaseModel):
    users: List[UserModel]


class MetaModel(BaseModel):
    result_count: int
    newest_id: Optional[int]
    oldest_id: Optional[int]


class SearchResult(BaseModel):
    meta: MetaModel
    includes: Optional[IncludesResult]
    data: Optional[List[TweetModel]]


def tweet_transformation():
    with open("data/raw/tweets.jsonl") as f:
        tweet_searches = f.readlines()

    user_df = pd.DataFrame(columns=["id", "name", "username"])
    tweet_df = pd.DataFrame(
        columns=[
            "id",
            "author_id",
            "created_at",
            "text",
            "retweet_count",
            "reply_count",
            "like_count",
            "quote_count",
        ]
    )

    for search_result in tweet_searches:
        result = SearchResult(**json.loads(search_result))

        if result.data is None:
            continue

        for user in result.includes.users:
            user_df = user_df.append(user.dict(), ignore_index=True)

        for tweet in result.data:
            metrics = tweet.public_metrics.dict()
            info = tweet.dict(exclude={"public_metrics"})

            info.update(metrics)

            tweet_df = tweet_df.append(info, ignore_index=True)

    outdir = "data/prepared"
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    user_df.to_csv("data/prepared/users.csv")
    tweet_df.to_csv("data/prepared/tweets.csv")


if __name__ == "__main__":
    tweet_transformation()
