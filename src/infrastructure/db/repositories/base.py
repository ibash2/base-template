from dataclasses import dataclass, field
from collections.abc import AsyncGenerator

import orjson
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from settings.config import Config


@dataclass
class SQLAlchemyRepo:
    _session: AsyncSession = field(
        default=None,
        kw_only=True,
        init=False,
    )


def build_sa_engine(config: Config) -> AsyncEngine:
    engine = create_async_engine(
        str(config.DATABASE_URL),
        echo=True,
        # echo_pool=config.echo,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=100,
    )
    return engine


def build_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(
        bind=engine, autoflush=False, expire_on_commit=False
    )
    return session_factory


async def build_sa_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
