from sqlalchemy import String, Integer, Numeric, BigInteger, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from decimal import Decimal
from typing import Optional, Final

from .session import Base


class UserInfo(Base):
    """
    DB의 user_info 테이블과 매핑되는 클래스

    Attributes:
        discord_user_id (int): 기본 키로 사용되는 Discord 사용자 ID

    DTO Relationships:
        account_info (AccountInfo): 사용자의 계정 정보를 나타내는 AccountInfo 모델과의 관계
        minecraft_player (MinecraftPlayerInfo): 사용자의 마인크래프트 정보를 나타내는 MinecraftPlayerInfo 모델과의 관계
    """

    __tablename__ = "user_info"

    discord_user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # 다른 DTO와의 관계 설정
    account_info = relationship("AccountInfo", back_populates="user_info", uselist=False)
    minecraft_player = relationship("MinecraftPlayerInfo", back_populates="user_info", uselist=False)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"{self.__class__.__name__}({attrs})"


class AccountInfo(Base):
    """
    DB의 account_info 테이블과 매핑되는 클래스

    Attributes:
        account_id (int): 기본 키로 사용되는 계정 ID
        discord_user_id (int): 외래 키로 사용되는 Discord 사용자 ID
        balance (int): 현재 금액
        last_check_in (int): 마지막으로 출석체크한 시간

    DTO Relationships:
        user_info (UserInfo): 사용자 정보를 나타내는 UserInfo 모델과의 관계
    """

    __tablename__ = "account_info"

    account_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    discord_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user_info.discord_user_id", ondelete="CASCADE", onupdate="CASCADE"), unique=True)
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 0), nullable=False, default=0, comment="현재 금액")
    last_check_in: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0, comment="마지막으로 출석체크한 시간")

    # 다른 DTO와의 관계 설정
    user_info = relationship("UserInfo", back_populates="account_info")

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"{self.__class__.__name__}({attrs})"

class MinecraftPlayerInfo(Base):
    """
    DB의 minecraft_player_info 테이블과 매핑되는 클래스

    Constants:
        MIN_USERNAME_LENGTH (int): Minecraft 닉네임의 최소 길이
        MAX_USERNAME_LENGTH (int): Minecraft 닉네임의 최대 길이

    Attributes:
        player_id (int): 기본 키로 사용되는 플레이어 ID
        discord_user_id (int): 외래 키로 사용되는 Discord 사용자 ID
        minecraft_username (Optional[str]): Minecraft 닉네임
        minecraft_uuid (Optional[str]): Minecraft UUID
        last_updated_at (int): 마지막으로 테이블이 업데이트된 시간

    DTO Relationships:
        user_info (UserInfo): 사용자 정보를 나타내는 UserInfo 모델과의 관계
    """

    MIN_USERNAME_LENGTH: Final[int] = 3
    MAX_USERNAME_LENGTH: Final[int] = 16

    __tablename__ = "minecraft_player_info"

    player_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    discord_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user_info.discord_user_id", ondelete="CASCADE", onupdate="CASCADE"), unique=True)
    minecraft_username: Mapped[Optional[str]] = mapped_column(String(16), unique=True, nullable=True, comment="마인크래프트 닉네임")
    minecraft_uuid: Mapped[Optional[str]] = mapped_column(String(36), unique=True, nullable=True, comment="고유 ID")
    last_updated_at: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0, comment="마지막으로 테이블이 업데이트된 시간")

    # 다른 DTO와의 관계 설정
    user_info = relationship("UserInfo", back_populates="minecraft_player")

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"{self.__class__.__name__}({attrs})"
