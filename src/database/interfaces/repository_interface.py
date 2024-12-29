from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Sequence


class IRepository[T](ABC):
    """DB Repository Interface"""

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[T]:
        """|coro|

        ID로 데이터를 가져옵니다.

        Args:
            entity_id (int): 데이터 ID

        Returns:
            Optional[T]: 데이터
        """
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: Optional[int] = 100) -> Sequence[T]:
        """|coro|

        모든 데이터를 가져옵니다.

        Args:
            skip (int, optional): 건너뛸 데이터 수. Defaults to 0.
            limit (Optional[int], optional): 최대 데이터 수. Defaults to 100.

        Returns:
            Sequence[T]: 모든 데이터
        """
        pass

    @abstractmethod
    def add(self, entity: T):
        """데이터를 추가합니다.

        Args:
            entity (T): 추가할 데이터
        """
        pass

    @abstractmethod
    async def update(self, entity: T):
        """|coro|

        데이터를 업데이트합니다.

        Args:
            entity (T): 업데이트할 데이터
        """
        pass

    @abstractmethod
    async def delete(self, entity: T):
        """|coro|

        데이터를 삭제합니다.

        Args:
            entity (T): 삭제할 데이터
        """
        pass
