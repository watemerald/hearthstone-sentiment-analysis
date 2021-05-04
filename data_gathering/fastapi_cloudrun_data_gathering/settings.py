import logging
from typing import Optional

from google.api_core.exceptions import GoogleAPIError
from google.auth.exceptions import GoogleAuthError
from google.cloud import secretmanager
from pydantic import BaseModel, BaseSettings

LOGGER = logging.getLogger(__name__)


class EnvSettings(BaseSettings):
    GCP_PROJECT: str
    GCP_BUCKET: str
    TWITTER_BEARER_TOKEN_SECRET: str = "TWITTER_BEARER_TOKEN"


settings = EnvSettings()


async def get_secret(name: str, *, project: Optional[str] = None) -> Optional[str]:
    if project is None:
        project = settings.GCP_PROJECT

    secret = f"projects/{project}/secrets/{name}/versions/latest"
    try:
        client = secretmanager.SecretManagerServiceAsyncClient()
        response = await client.access_secret_version(name=secret)
        return response.payload.data.decode()
    except (GoogleAuthError, GoogleAPIError) as e:
        LOGGER.error(f"Could not fetch ({name}) from GCS: {e}")


class AppSettings(BaseModel):
    GCP_PROJECT: str
    TWITTER_BEARER_TOKEN: str


async def get_app_settings() -> AppSettings:
    twitter_token = await get_secret(settings.TWITTER_BEARER_TOKEN_SECRET)

    return AppSettings(
        GCP_PROJECT=settings.GCP_PROJECT, TWITTER_BEARER_TOKEN=twitter_token
    )
