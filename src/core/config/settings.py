from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


def get_model_config(env_prefix: str = "") -> SettingsConfigDict:
    env_file = BASE_DIR / ".env"

    return SettingsConfigDict(env_file=env_file, env_prefix=env_prefix, extra="allow")


class IntegrationAPI(BaseSettings):
    CURRENCY_API_URL: str = "https://cbr.ru/scripts/XML_daily.asp"


class RabbitMQ(BaseSettings):
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"


class RedisSettings(BaseSettings):
    HOST: str = "redis"
    PORT: int = 6379
    DATA_DB: int = 2

    @property
    def URL(self):
        return f"redis://{self.HOST}:{self.PORT}"

    model_config = get_model_config("REDIS_")


class Settings(BaseSettings):
    BASE_DIR: Path = BASE_DIR
    API: IntegrationAPI = IntegrationAPI()
    RABBITMQ: RabbitMQ = RabbitMQ()
    REDIS: RedisSettings = RedisSettings()

    model_config = get_model_config("")


settings = Settings()
