import json
from typing import List

from fastapi import BackgroundTasks, FastAPI

from .search import search_tweets
from .tasks import upload_to_gcs

app = FastAPI()


async def get_tweets_and_upload_data(users: List[str], hashtags: List[str]):
    responses = await search_tweets(users, hashtags)
    text = "\n".join((json.dumps(response) for response in responses))
    upload_to_gcs(text)


@app.post("/get_tweets")
async def get_tweets(
    users: List[str], hashtags: List[str], background_tasks: BackgroundTasks
):
    background_tasks.add_task(get_tweets_and_upload_data, users, hashtags)
    return {"message": "Started gathering tweets from last week"}


@app.get("/")
async def root():
    return {"message": "POST to /get_tweets to start loading tweets"}
