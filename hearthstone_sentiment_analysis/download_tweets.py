from google.cloud import storage
from pydantic import BaseSettings


class Settings(BaseSettings):
    GCP_BUCKET: str

    class Config:
        env_file = ".env"


settings = Settings()


def download_files():
    client = storage.Client()
    blobs = client.list_blobs(settings.GCP_BUCKET)

    with open("data/raw/tweets.jsonl", "w") as f:
        for blob in blobs:
            f.write(blob.download_as_text())


if __name__ == "__main__":
    download_files()
