import logging
from typing import Optional

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class EnvConfig(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"

    ODDS_API_KEY: Optional[str] = None
    APIFOOTBALL_API_KEY: Optional[str] = None
    AVANGENIO_API_KEY: Optional[str] = None
    TELEGRAM_TOKEN: Optional[str] = None
    NGROK_TOKEN: Optional[str] = None

    URL_BOT: Optional[str] = None
    ENV: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False


config = EnvConfig()

if __name__ == "__main__":
    print(config.ENV)
    print(config.URL_BOT)
    print(config.DATABASE_URL)
