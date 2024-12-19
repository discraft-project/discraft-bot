from dotenv import dotenv_values
from dataclasses import dataclass
from typing import Union, Optional, Any, get_origin, get_args
from types import UnionType


class UnsupportedTypeConversionError(Exception):
    """환경 변수의 타입 변환이 지원되지 않을 때 발생하는 예외"""
    pass


@dataclass(frozen=True)
class Environment:
    """환경변수를 관리하는 클래스"""
    DISCORD_BOT_TOKEN: str
    DISCORD_BOT_PREFIX: str
    DISCORD_BOT_ACTIVITY: Optional[str]
    DISCORD_GUILD_ID: Optional[int]
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PORT: int
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    LOG_LEVEL: str

    @classmethod
    def from_env(cls, env_path: str = ".env") -> "Environment":
        """환경변수를 .env 파일에서 가져옵니다."""
        environ = dotenv_values(env_path)
        overrides: dict[str, Any] = {}

        for key, _type in cls.__annotations__.items():
            # Union 타입인 경우 (Optional 포함)
            if get_origin(_type) in (Union, UnionType):
                type_args = get_args(_type)
                if len(type_args) == 2 and type(None) in type_args:
                    _type = next(arg for arg in type_args if arg is not type(None))
                    if key not in environ or environ[key] == "":  # 환경변수가 없거나 비어있는 경우
                        overrides[key] = None
                        continue
                else:
                    raise UnsupportedTypeConversionError("환경변수는 여러 타입의 형변환을 지원하지 않습니다.")

            # 환경변수가 없거나 비어있는 경우
            if key not in environ:
                raise ValueError(f"환경변수 {key}가 없습니다.")

            elif environ[key] == "":
                raise ValueError(f"환경변수 {key}가 비어있습니다.")

            # 타입 변환
            try:
                overrides[key] = _type(environ[key])
            except ValueError:
                raise ValueError(f"환경변수 {key}의 값 '{environ[key]}'을(를) {_type.__name__} 타입으로 변환할 수 없습니다.")

        return cls(**overrides)


class EnviromentSingleton:
    """환경변수 싱글톤 클래스"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = Environment.from_env()
        return cls._instance

# 환경변수
ENV = EnviromentSingleton()
