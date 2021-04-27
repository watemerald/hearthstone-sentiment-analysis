from pydantic import BaseSettings


class Settings(BaseSettings):
    TWITTER_BEARER_TOKEN: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()