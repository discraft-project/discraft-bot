from decouple import config
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Environment:
    """환경변수를 관리하는 클래스"""
    DISCORD_BOT_TOKEN: str = config("DISCORD_BOT_TOKEN")                                 # type: ignore
    DISCORD_BOT_PREFIX: str = config("DISCORD_BOT_PREFIX")                               # type: ignore
    DISCORD_BOT_ACTIVITY: Optional[str] = config("DISCORD_BOT_ACTIVITY", default=None)   # type: ignore
    DISCORD_GUILD_ID: Optional[str] = config("DISCORD_GUILD_ID", default=None)           # type: ignore
    MYSQL_HOST: str = config("MYSQL_HOST")                                               # type: ignore
    MYSQL_USER: str = config("MYSQL_USER")                                               # type: ignore
    MYSQL_PORT: int = config("MYSQL_PORT", default=3306, cast=int)                       # type: ignore
    MYSQL_PASSWORD: str = config("MYSQL_PASSWORD")                                       # type: ignore
    MYSQL_DB_NAME: str = config("MYSQL_DB_NAME")                                         # type: ignore
    LOG_LEVEL: str = config("LOG_LEVEL", default="INFO")                                 # type: ignore

    def __post_init__(self):
        for key, value in self.__dict__.items():
            if isinstance(value, str) and value == "":
                raise ValueError(f"환경변수 {key}가 비어있습니다.")

# 환경변수
ENV = Environment()
