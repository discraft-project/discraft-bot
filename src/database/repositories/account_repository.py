from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Sequence

from ..interfaces import IRepository
from ..models import AccountInfo


class AccountRepository(IRepository[AccountInfo]):
    """AccountInfo 데이터베이스 Repository 클래스

    Args:
        IRepository ([AccountInfo]): IRepository 상속
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: int) -> Optional[AccountInfo]:
        """|coro|

        entity_id로 데이터를 가져옵니다.

        Args:
            entity_id (int): discord 사용자 ID

        Returns:
            Optional[AccountInfo]: 데이터
        """
        result = await self.session.execute(
            select(AccountInfo).filter(AccountInfo.discord_user_id == entity_id)
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: Optional[int] = 100) -> Sequence[AccountInfo]:
        """|coro|

        모든 데이터를 가져옵니다.

        Args:
            skip (int, optional): 건너뛸 데이터 수. Defaults to 0.
            limit (Optional[int], optional): 최대 데이터 수. Defaults to 100.

        Returns:
            Sequence[AccountInfo]: 모든 데이터
        """
        result = await self.session.execute(
            select(AccountInfo).offset(skip).limit(limit)
        )
        return result.scalars().all()

    def add(self, entity: AccountInfo):
        """데이터를 추가합니다.
        
        Args:
            entity (AccountInfo): 추가할 데이터
        """
        self.session.add(entity)

    async def update(self, entity: AccountInfo):
        """|coro|

        데이터를 업데이트합니다.

        Args:
            entity (AccountInfo): 업데이트할 데이터
        """
        await self.session.merge(entity)

    async def delete(self, entity: AccountInfo):
        """|coro|

        데이터를 삭제합니다.

        Args:
            entity (AccountInfo): 삭제할 데이터
        """
        await self.session.delete(entity)
