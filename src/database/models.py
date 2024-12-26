from sqlalchemy import Column, BigInteger, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from .session import Base


class UserInfo(Base):
    """
    DB의 user_info 테이블과 매핑되는 클래스
    Attributes:
        discord_user_id (int): 기본 키로 사용되는 Discord 사용자 ID
        mc_user_name (str | None): 고유하고 인덱싱된 Minecraft 사용자 이름
        mc_uuid (str | None): 고유하고 인덱싱된 Minecraft UUID
        account (AccountInfo): 사용자의 계정 정보를 나타내는 AccountInfo 모델과의 관계
    """

    __tablename__ = "user_info"

    discord_user_id = Column(BigInteger, primary_key=True)
    mc_user_name: Column[str | None] = Column(String(16), unique=True, index=True, nullable=True)  # type: ignore
    mc_uuid: Column[str | None] = Column(String(36), unique=True, index=True, nullable=True)       # type: ignore
    account = relationship("AccountInfo", back_populates="user", uselist=False)

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
        user (UserInfo): 사용자 정보를 나타내는 UserInfo 모델과의 관계
    """

    __tablename__ = "account_info"

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    discord_user_id = Column(BigInteger, ForeignKey("user_info.discord_user_id", ondelete="CASCADE", onupdate="CASCADE"), unique=True, index=True)
    balance = Column(Numeric(18, 0), nullable=False, default=0, comment="현재 금액")
    last_check_in = Column(BigInteger, nullable=False, default=0, comment="마지막으로 출석체크한 시간")
    user = relationship("UserInfo", back_populates="account", uselist=False)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"{self.__class__.__name__}({attrs})"
