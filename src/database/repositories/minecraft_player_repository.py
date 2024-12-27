from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Sequence

from ..interfaces import IRepository
from ..models import MinecraftPlayerInfo


class MinecraftPlayerRepository(IRepository[MinecraftPlayerInfo]):
    """MinecraftPlayerInfo 데이터베이스 Repository 클래스

    Args:
        IRepository ([MinecraftPlayerInfo]): IRepository 상속
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[MinecraftPlayerInfo]:
        """|coro|

        user_id로 데이터를 가져옵니다.

        Args:
            user_id (int): discord 사용자 ID

        Returns:
            Optional[MinecraftPlayerInfo]: 데이터
        """
        result = await self.session.execute(
            select(MinecraftPlayerInfo).filter(MinecraftPlayerInfo.discord_user_id == user_id)
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: Optional[int] = 100) -> Sequence[MinecraftPlayerInfo]:
        """|coro|

        모든 데이터를 가져옵니다.

        Args:
            skip (int, optional): 건너뛸 데이터 수. Defaults to 0.
            limit (Optional[int], optional): 최대 데이터 수. Defaults to 100.

        Returns:
            Sequence[MinecraftPlayerInfo]: 모든 데이터
        """
        result = await self.session.execute(
            select(MinecraftPlayerInfo).offset(skip).limit(limit)
        )
        return result.scalars().all()

    def add(self, entity: MinecraftPlayerInfo):
        """데이터를 추가합니다.
        
        Args:
            entity (MinecraftPlayerInfo): 추가할 데이터
        """
        self.session.add(entity)

    async def update(self, entity: MinecraftPlayerInfo):
        """|coro|

        데이터를 업데이트합니다.

        Args:
            entity (MinecraftPlayerInfo): 업데이트할 데이터
        """
        await self.session.merge(entity)

    async def delete(self, entity: MinecraftPlayerInfo):
        """|coro|

        데이터를 삭제합니다.

        Args:
            entity (MinecraftPlayerInfo): 삭제할 데이터
        """
        await self.session.delete(entity)
