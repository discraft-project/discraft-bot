from sqlalchemy import Column, BigInteger, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional

from .session import Base


class UserInfo(Base):
    """
    DB의 user_info 테이블과 매핑되는 클래스
    Attributes:
        discord_user_id (int): 기본 키로 사용되는 Discord 사용자 ID
        account_info (AccountInfo): 사용자의 계정 정보를 나타내는 AccountInfo 모델과의 관계
        minecraft_player (MinecraftPlayerInfo): 사용자의 마인크래프트 정보를 나타내는 MinecraftPlayerInfo 모델과의 관계
    """

    __tablename__ = "user_info"

    discord_user_id = Column(BigInteger, primary_key=True)

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
        user_info (UserInfo): 사용자 정보를 나타내는 UserInfo 모델과의 관계
    """

    __tablename__ = "account_info"

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    discord_user_id = Column(BigInteger, ForeignKey("user_info.discord_user_id", ondelete="CASCADE", onupdate="CASCADE"), unique=True)
    balance = Column(Numeric(18, 0), nullable=False, default=0, comment="현재 금액")
    last_check_in = Column(BigInteger, nullable=False, default=0, comment="마지막으로 출석체크한 시간")

    # 다른 DTO와의 관계 설정
    user_info = relationship("UserInfo", back_populates="account_info")

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"{self.__class__.__name__}({attrs})"

class MinecraftPlayerInfo(Base):
    """
    DB의 minecraft_player_info 테이블과 매핑되는 클래스
    Attributes:
        player_id (int): 기본 키로 사용되는 플레이어 ID
        discord_user_id (int): 외래 키로 사용되는 Discord 사용자 ID
        minecraft_username (Optional[str]): Minecraft 닉네임
        minecraft_uuid (Optional[str]): Minecraft UUID
        last_updated_at (int): 마지막으로 테이블이 업데이트된 시간
        user_info (UserInfo): 사용자 정보를 나타내는 UserInfo 모델과의 관계
    """

    __tablename__ = "minecraft_player_info"

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    discord_user_id = Column(BigInteger, ForeignKey("user_info.discord_user_id", ondelete="CASCADE", onupdate="CASCADE"), unique=True)
    minecraft_username: Column[Optional[str]] = Column(String(16), unique=True, nullable=True, comment="마인크래프트 닉네임")  # type: ignore
    minecraft_uuid: Column[Optional[str]] = Column(String(36), unique=True, nullable=True, comment="고유 ID")                 # type: ignore
    last_updated_at = Column(BigInteger, nullable=False, default=0, comment="마지막으로 테이블이 업데이트된 시간")

    # 다른 DTO와의 관계 설정
    user_info = relationship("UserInfo", back_populates="minecraft_player")

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"{self.__class__.__name__}({attrs})"
