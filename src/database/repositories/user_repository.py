from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Sequence

from ..interfaces import IRepository
from ..models import UserInfo


class UserRepository(IRepository[UserInfo]):
    """UserInfo 데이터베이스 Repository 클래스

    Args:
        IRepository ([UserInfo]): IRepository 상속
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: int) -> Optional[UserInfo]:
        """|coro|

        entity_id로 데이터를 가져옵니다.

        Args:
            entity_id (int): discord 사용자 ID

        Returns:
            Optional[UserInfo]: 데이터
        """
        result = await self.session.execute(
            select(UserInfo).filter(UserInfo.discord_user_id == entity_id)
        )
        return result.scalars().first()

    async def get_by_mc_name(self, mc_name: str) -> Optional[UserInfo]:
        """|coro|

        Minecraft 사용자 이름으로 데이터를 가져옵니다.

        Args:
            mc_name (str): 마인크래프트 사용자 이름

        Returns:
            Optional[UserInfo]: 데이터
        """
        result = await self.session.execute(
            select(UserInfo).filter(UserInfo.minecraft_player.has(minecraft_username=mc_name))
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: Optional[int] = 100) -> Sequence[UserInfo]:
        """|coro|

        모든 데이터를 가져옵니다.

        Args:
            skip (int, optional): 건너뛸 데이터 수. Defaults to 0.
            limit (Optional[int], optional): 최대 데이터 수. Defaults to 100.

        Returns:
            Sequence[UserInfo]: 모든 데이터
        """
        result = await self.session.execute(
            select(UserInfo).offset(skip).limit(limit)
        )
        return result.scalars().all()

    def add(self, entity: UserInfo):
        """데이터를 추가합니다.

        Args:
            entity (UserInfo): 추가할 데이터
        """
        self.session.add(entity)

    async def update(self, entity: UserInfo):
        """|coro|

        데이터를 업데이트합니다.

        Args:
            entity (UserInfo): 업데이트할 데이터
        """
        await self.session.merge(entity)

    async def delete(self, entity: UserInfo):
        """|coro|

        데이터를 삭제합니다.

        Args:
            entity (UserInfo): 삭제할 데이터
        """
        await self.session.delete(entity)
