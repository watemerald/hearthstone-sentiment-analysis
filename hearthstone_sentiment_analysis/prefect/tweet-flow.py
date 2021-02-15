from prefect import task, Flow, unmapped
import prefect
from prefect.engine.signals import FAIL
from prefect.tasks.secrets import EnvVarSecret

import requests


from typing import Dict, List


@task
def get_users() -> List[str]:
    with open("data/twitter_users.txt") as f:
        users = f.readlines()
    return users


@task
def load_tweets(user: str, twitter_token: str) -> Dict:
    re = requests.get(
        "https://api.twitter.com/2/tweets/search/recent",
        params={
            "query": f"from:{user} -is:retweet",
            "max_results": 50,
        },
        headers={"Authorization": f"Bearer {twitter_token}"},
    )

    if re.status_code != 200:
        raise FAIL(f"Failed to load tweets for user {user}")

    return re.json()


@task
def get_tweet_text(tweet: Dict) -> str:
    return tweet["data"]["text"]


@task
def save_tweets(tweets: List[str]) -> None:
    with open("tweets.txt", "w") as f:
        f.write("\n".join(tweets))


with Flow("load tweets") as flow:
    twitter_token = EnvVarSecret("TWITTER_TOKEN")
    users = get_users()
    tweets = load_tweets.map(users, twitter_token=unmapped(twitter_token))
    tweet_texts = get_tweet_text.map(tweets)
    save_tweets(tweet_texts)

flow.register(project_name="Hearthstone Sentiment Analysis")