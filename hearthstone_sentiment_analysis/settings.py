from pydantic import BaseSettings


class Settings(BaseSettings):
    GCP_PROJECT: str
    GCP_BUCKET: str

    class Config:
        env_file = ".env"


settings = Settings()
