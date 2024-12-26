import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    async_scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("discord.database.session")
Base = declarative_base()


class DiscraftDBConnection:
    """비동기 데이터베이스 연결을 위한 클래스"""

    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
        drivername: str = "mysql+aiomysql",
    ):
        """DatabaseConnection 클래스 생성자

        Args:
            drivername (str, optional): SQLAlchemy 드라이버 이름.
            username (str): database 사용자 이름
            password (str): database 비밀번호
            host (str): database 호스트 주소
            port (int): database 포트
            database (str): database 이름
        """
        self.connection_string = URL.create(
            drivername=drivername,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )

        self.engine = None
        self.session_factory = None
        self.session = None

    async def initialize(self):
        """database에 연결합니다.

        다른 메서드를 호출하기 전에 먼저 호출해야 합니다.
        """
        logger.info(f"Initializing database connection to {self.connection_string}")
        try:
            self.engine = create_async_engine(
                self.connection_string,

                # SQL 문을 출력 (디버깅용)
                echo=__debug__ and logging.getLogger().level <= logging.DEBUG,

                # 커넥션 풀 설정
                pool_size=5,
                max_overflow=10,

                # 커넥션이 유효한지 확인
                pool_pre_ping=True,
            )
        except SQLAlchemyError as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
        else:
            logger.info("Database connection established")

        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,

            # 커밋 후에도 세션을 유지
            expire_on_commit=False,

            # autoflush를 비활성화하여 성능 향상
            autoflush=False,
        )
        self.session = async_scoped_session(self.session_factory, scopefunc=asyncio.current_task)

    async def get_session(self) -> AsyncSession:
        """비동기 세션을 반환합니다.

        세션을 사용한 후에는 반드시 `commit()` 또는 `rollback()`후 `close()`를 호출해야 합니다.

        Returns:
            AsyncSession: 비동기 세션
        """
        if self.session is None:
            raise RuntimeError("DatabaseConnection not initialized. Call initialize() first.")
        return self.session()

    @asynccontextmanager
    async def session_scope(self) -> AsyncGenerator[AsyncSession, None]:
        """비동기 세션을 사용하는 컨텍스트 매니저입니다.

        Examples:
        ```python
        db = DatabaseConnection(...)
        async with db.session_scope() as session:
            async with session.begin():  # transaction 시작
                ... # session을 사용하는 코드
        ```
        """
        session = await self.get_session()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close(self):
        """database 연결을 종료합니다."""
        if self.engine is not None:
            logger.info(f"Closing database connection to {self.connection_string}")
            await self.engine.dispose()
        else:
            logger.warning("Database connection is not initialized")
