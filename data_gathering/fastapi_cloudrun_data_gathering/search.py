import asyncio
from typing import Dict, List, Tuple

import httpx
from fastapi import Depends

from .settings import AppSettings, get_app_settings


async def search_tweets(
    users: List[str],
    hashtags: List[str],
    *,
    max_results: int = 100,
    settings: AppSettings = Depends(get_app_settings),
) -> Tuple[Dict]:
    headers = {"Authorization": f"Bearer {settings.TWITTER_BEARER_TOKEN}"}

    async with httpx.AsyncClient(headers=headers) as client:

        async def twitter_search(query: str) -> Dict:
            response = await client.get(
                "https://api.twitter.com/2/tweets/search/recent",
                params={
                    "query": query,
                    "max_results": max_results,
                    "expansions": "author_id",
                    "tweet.fields": "public_metrics,created_at",
                },
            )
            return response.json()

        user_querys = [
            twitter_search(
                query=f"from:{user} -is:retweet",
            )
            for user in users
        ]
        hashtag_querys = [
            twitter_search(
                query=f"#{hashtag} -is:retweet",
            )
            for hashtag in hashtags
        ]

        responses = await asyncio.gather(*user_querys, *hashtag_querys)
        return responses
